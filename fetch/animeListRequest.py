import time

import requests
import json
from requests.exceptions  import HTTPError
import logging
from authentication import auth
import os

code = "" # TODO: get it form env file
users = [] # TODO: get it from env file
testAnime = {'id': "test",
             'title': "test",
             'picture': "test"}
episode_req = 0
min_req = 0
movie_min_req = 0

def get_anime_list(user, url=''):
    payload = {'status': 'completed',
               'sort': 'anime_title',
               'limit': 1000,
               'nsfw': 'true'}
    headers = {'Authorization': f'Bearer {auth.get_access_token()}'}

    if url == '':
        url = f"" # TODO: get it from env file

    anime_list_request = requests.get(url, params=payload, headers=headers)

    try:
        anime_list_request.raise_for_status()

        data = anime_list_request.json()
        get_animes_from_json(data, user)
    except HTTPError as e:
        if e.response.status_code == 401 and e.response.json()['error'] == 'invalid_token':
            logging.warning("Refresh token expired, refereshing token")
            #auth.refresh_token("TODO")
        else:
            logging.error(f"{e.response.status_code} {e.response.text}")


def get_animes_from_json(json_data, user):
    length = -1
    anime_add_list = []
    anime_json = {}
    watched_anime_ids = []

    #time.sleep(.4)

    try:
        length = len(json_data['data'])
    except Exception as e:
        print(f"Querry error: {e}")

    try:
        with open('anime_datas.json', 'r') as read_anime_datas:
            anime_json = json.load(read_anime_datas)
    except Exception as e:
        with open("anime_datas.json", 'w') as create_anime_datas:
            print(f"anime_datas.json not found: {e}")
            json.dump({}, create_anime_datas, indent=4)

    try:
        for i in range(length):
            anime_id = json_data['data'][i]['node']['id']
            print(f"anime_id: {anime_id} , watched by: {user}")
            watched_anime_ids.append(str(anime_id))
            if str(anime_id) not in anime_json:
                anime_data = querry_anime_by_id(anime_id)
                anime_add_list.append(anime_data)
    except Exception as e:
        print(f"Error occurred while processing anime data: {e}")

    write_anime_into_json(anime_add_list)
    write_user_into_json(user, watched_anime_ids)

    try:
        url = json_data['paging']['next']
        get_anime_list(user, url)
    except Exception as e:
        print(f'Error occured/ got the last anime {e}')


def write_anime_into_json(anime_list):
    anime_data = {}

    try:
        with open('anime_datas.json', 'r') as read:
            anime_data = json.load(read)
    except FileNotFoundError as e:
        with open('anime_datas.json', 'w') as create:
            json.dump(anime_data, create, indent=4)

    for data in anime_list:
        if str(data['id']) not in anime_data:
            anime_data[str(data['id'])] = format_anime_data(data)

    with open('anime_datas.json', 'w') as write_animes:
        json.dump(anime_data, write_animes, indent=4)


def get_uniques():
    ret = {}

    for user in users:
        ret[user] = {"animes": [],
                     "unique": 0,
                     "completed": 0}

    with open('anime_datas.json', 'r') as read_anime:
        anime_data = json.load(read_anime)
    with open('anime_users.json', 'r') as read_ids:
        user_ids = json.load(read_ids)

    for anime_id in user_ids:
        if len(user_ids[str(anime_id)]) < 2 and check_requirements_anime(anime_data[anime_id]):
            ret[user_ids[str(anime_id)][0]]['animes'].append(anime_data[str(anime_id)])
            ret[user_ids[str(anime_id)][0]]['completed'] += 1
            ret[user_ids[str(anime_id)][0]]['unique'] += 1
        else:
            for user in user_ids[str(anime_id)]:
                ret[user]['completed'] += 1

    return ret


def querry_animes():
    for user in users:
        get_anime_list(user)


def querry_user(user):
    url = f"https://api.jikan.moe/v4/users/{user}"
    querry = requests.get(url)
    json_data = querry.json()
    return json_data["data"]["images"]["jpg"]["image_url"]


def get_users():
    return users


def check_requirements_anime(anime_data):
    global min_req, episode_req, movie_min_req

    #duriaton_at_least = 5400

    #ret1 = anime_data['num_episodes'] >= 4 or anime_data['media_type'] == 'movie'
    #ret2 = anime_data['num_episodes'] * anime_data['average_episode_duration'] >= duriaton_at_least
    #ret3 = (anime_data['num_episodes'] * anime_data['average_episode_duration'] >= duriaton_at_least or
    #        anime_data['media_type'] == 'movie')

    return anime_data['episodes'] >= 4 or anime_data['media'] == 'movie'


def querry_anime_by_id(anime_id):
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}"
    payload = "fields=media_type,num_episodes,average_episode_duration,mean"
    headers = {'Authorization': f'Bearer {auth.get_access_token()}'}

    anime_request = requests.get(url, params=payload, headers=headers)
    time.sleep(0.2)
    if anime_request.status_code == 200:
        print(anime_request.json())
        return anime_request.json()
    elif anime_request.status_code == 503:
        print(anime_request.status_code)
        print("503 Error in : querry_anime_by_id")
        querry_anime_by_id(anime_id)
    else:
        print(f"Error occurred while processing anime data: {anime_id}")
        print(anime_request.status_code)


def format_anime_data(anime_data):
    formatted_anime_data = {'id': anime_data['id'],
                            'title': anime_data['title'],
                            'picture': anime_data['main_picture']['medium'],
                            'media': anime_data['media_type'],
                            'episodes': anime_data['num_episodes'],
                            'episode_duration': anime_data['average_episode_duration'],
                            'rating': anime_data['mean']}

    return formatted_anime_data


def write_user_into_json(user, watched_anime_ids):
    animes_watched_by_user = {}

    try:
        with open('anime_users.json', 'r') as read:
            animes_watched_by_user = json.load(read)
    except FileNotFoundError as e:
        with open('anime_users.json', 'w') as create:
            json.dump({}, create, indent=4)

    for anime_id in watched_anime_ids:
        if str(anime_id) not in animes_watched_by_user:
            animes_watched_by_user[str(anime_id)] = [user]
        else:
            animes_watched_by_user[str(anime_id)].append(user)

    with open('anime_users.json', 'w') as write_user:
        json.dump(animes_watched_by_user, write_user, indent=4)