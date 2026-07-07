import time

import requests
from requests.exceptions  import HTTPError
import logging
from authentication import auth
from firebase.firestore import FirestoreClient

fs = FirestoreClient()
import os

users = [u.strip() for u in os.environ.get('MAL_USERS', '').split(',') if u.strip()]
ANIMELIST_URL_TEMPLATE = os.environ.get(
    'MAL_ANIMELIST_URL',
    'https://api.myanimelist.net/v2/users/{user}/animelist'
)
testAnime = {'id': "test",
             'title': "test",
             'picture': "test"}
episode_req = 0
min_req = 0
movie_min_req = 0

anime_cache = {}
animes_watched_by_user = {}
new_animes = []

def get_anime_list(user, url='', retries=3):
    payload = {'status': 'completed',
               'sort': 'anime_title',
               'limit': 1000,
               'nsfw': 'true'}
    headers = {'Authorization': f'Bearer {auth.get_access_token()}'}

    if url == '':
        url = ANIMELIST_URL_TEMPLATE.format(user=user)

    try:
        anime_list_request = requests.get(url, params=payload, headers=headers, timeout=30)
    except requests.exceptions.RequestException as e:
        if retries > 0:
            wait = 2 ** (4 - retries)
            print(f"Network error for user {user}: {e}. Retrying in {wait}s ({retries} left)")
            time.sleep(wait)
            return get_anime_list(user, url=url, retries=retries - 1)
        print(f"Giving up on user {user} after network failures: {e}")
        return

    time.sleep(1.0)
    try:
        anime_list_request.raise_for_status()

        data = anime_list_request.json()
        get_animes_from_json(data, user)
    except HTTPError as e:
        if e.response.status_code == 401 and e.response.json()['error'] == 'invalid_token':
            # The token is refreshed once at the start of execute.py, so a 401 here
            # means even the fresh token is invalid (e.g. the refresh_token expired).
            logging.warning("Access token invalid; re-run authentication/generate_token.py to reseed MAL_TOKEN")
        else:
            logging.error(f"{e.response.status_code} {e.response.text}")


def get_animes_from_json(json_data, user):
    length = -1
    watched_anime_ids = []

    try:
        length = len(json_data['data'])
    except Exception as e:
        print(f"Querry error: {e}")

    try:
        for i in range(length):
            anime_id = json_data['data'][i]['node']['id']
            print(f"anime_id: {anime_id} , watched by: {user}")
            watched_anime_ids.append(str(anime_id))
            if str(anime_id) not in anime_cache:
                anime_data = querry_anime_by_id(anime_id)
                if anime_data is not None:
                    formatted = format_anime_data(anime_data)
                    anime_cache[str(anime_id)] = formatted
                    new_animes.append(formatted)
    except Exception as e:
        print(f"Error occurred while processing anime data: {e}")

    add_user_watched_animes(user, watched_anime_ids)

    try:
        url = json_data['paging']['next']
        get_anime_list(user, url)
    except Exception as e:
        print(f'Error occured/ got the last anime {e}')


def get_uniques():
    ret = {}

    for user in users:
        ret[user] = {"animes": [],
                     "unique": 0,
                     "completed": 0}

    for anime_id, watchers in animes_watched_by_user.items():
        if len(watchers) < 2 and check_requirements_anime(anime_cache[anime_id]):
            ret[watchers[0]]['animes'].append(anime_cache[anime_id])
            ret[watchers[0]]['completed'] += 1
            ret[watchers[0]]['unique'] += 1
        else:
            for user in watchers:
                ret[user]['completed'] += 1

    return ret


def querry_animes():
    global anime_cache, animes_watched_by_user, new_animes
    anime_cache = fs.get_anime_cache()
    animes_watched_by_user = {}
    new_animes = []

    for user in users:
        get_anime_list(user)

    fs.upload_anime_cache(new_animes)


def querry_user(user, retries=3):
    url = f"https://api.jikan.moe/v4/users/{user}"
    try:
        querry = requests.get(url, timeout=30)
        querry.raise_for_status()
        json_data = querry.json()
        return json_data["data"]["images"]["jpg"]["image_url"]
    except (requests.exceptions.RequestException, KeyError) as e:
        if retries > 0:
            wait = 2 ** (4 - retries)
            print(f"Network error fetching pfp for {user}: {e}. Retrying in {wait}s ({retries} left)")
            time.sleep(wait)
            return querry_user(user, retries - 1)
        print(f"Giving up on pfp for {user}: {e}")
        return None

def get_users():
    return users


def check_requirements_anime(anime_data):
    global min_req, episode_req, movie_min_req
    return anime_data['episodes'] >= 4 or anime_data['media'] == 'movie'


def querry_anime_by_id(anime_id, retries=3):
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}"
    payload = "fields=media_type,num_episodes,average_episode_duration,mean"
    headers = {'Authorization': f'Bearer {auth.get_access_token()}'}

    try:
        anime_request = requests.get(url, params=payload, headers=headers, timeout=30)
    except requests.exceptions.RequestException as e:
        if retries > 0:
            wait = 2 ** (4 - retries)
            print(f"Network error for anime {anime_id}: {e}. Retrying in {wait}s ({retries} left)")
            time.sleep(wait)
            return querry_anime_by_id(anime_id, retries - 1)
        print(f"Giving up on anime {anime_id} after network failures: {e}")
        return None

    time.sleep(1.0)
    if anime_request.status_code == 200:
        print(anime_request.json())
        return anime_request.json()
    elif anime_request.status_code in (429, 500, 502, 503, 504) and retries > 0:
        wait = 2 ** (4 - retries)
        print(f"{anime_request.status_code} on anime {anime_id}, retrying in {wait}s ({retries} left)")
        time.sleep(wait)
        return querry_anime_by_id(anime_id, retries - 1)
    else:
        print(f"Error occurred while processing anime data: {anime_id}, status: {anime_request.status_code}, body: {anime_request.text[:200]}")
        return None


def format_anime_data(anime_data):
    formatted_anime_data = {'id': anime_data['id'],
                            'title': anime_data['title'],
                            'picture': anime_data['main_picture']['medium'],
                            'media': anime_data['media_type'],
                            'episodes': anime_data['num_episodes'],
                            'episode_duration': anime_data['average_episode_duration'],
                            'rating': anime_data['mean']}

    return formatted_anime_data


def add_user_watched_animes(user, watched_anime_ids):
    for anime_id in watched_anime_ids:
        key = str(anime_id)
        if key not in animes_watched_by_user:
            animes_watched_by_user[key] = [user]
        else:
            animes_watched_by_user[key].append(user)