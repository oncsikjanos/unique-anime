import time

import animeListRequest
from firebase import firestore as fs
import json

users_data = {}

if __name__ == "__main__":

    with open('anime_users.json', 'w') as file:
        json.dump({}, file, indent=4)

    animeListRequest.querry_animes()
    users_data = animeListRequest.get_uniques()

    fs.clear_out_users()

    for user_data in users_data:

        fs.upload_anime_data(users_data[user_data]['animes'], user_data)
        time.sleep(0.4)

        pfp = animeListRequest.querry_user(user_data)
        user = {'name': user_data,
                'pfp': pfp,
                'completed': users_data[user_data]['completed'],
                'unique': users_data[user_data]['unique']}
        fs.upload_user_data(user)
