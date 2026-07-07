import time

import animeListRequest
from authentication import auth
from firebase.firestore import FirestoreClient

fs = FirestoreClient()
users_data = {}

if __name__ == "__main__":

    # Rotate the MAL token first: this writes the new token to token_myanimelist.json
    # so the workflow can push it back into the MAL_TOKEN secret even if the fetch
    # below fails afterwards.
    auth.refresh_access_token()

    existing_pfps = {}
    for doc in fs.db.collection("User").stream():
        d = doc.to_dict() or {}
        name = d.get('name')
        pfp = d.get('pfp')
        if name and pfp:
            existing_pfps[name] = pfp

    animeListRequest.querry_animes()
    users_data = animeListRequest.get_uniques()

    fs.clear_out_users()

    for user_data in users_data:

        fs.upload_anime_data(users_data[user_data]['animes'], user_data)
        time.sleep(0.4)

        pfp = existing_pfps.get(user_data) or animeListRequest.querry_user(user_data)
        user = {'name': user_data,
                'pfp': pfp,
                'completed': users_data[user_data]['completed'],
                'unique': users_data[user_data]['unique']}
        fs.upload_user_data(user)
    
    fs.update_last_updated()
