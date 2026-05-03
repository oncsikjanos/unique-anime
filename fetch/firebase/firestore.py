import json
import os

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from google.cloud.firestore_v1 import FieldFilter, DocumentSnapshot
from model.anime import Anime
from model.user import User

service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
if not service_account_json:
    raise EnvironmentError('FIREBASE_SERVICE_ACCOUNT environment variable is not set')

cred = credentials.Certificate(json.loads(service_account_json))
firebase_admin.initialize_app(cred)
db = firestore.client()


def upload_user_data(user_data):
    doc_ref = db.collection('User').document()
    doc_ref.set(user_data)


def upload_anime_data(anime_list, user):
    batch = db.batch()
    collection_ref = db.collection("Anime").document(user).collection("Uniques")
    clear_out_collection(collection_ref)

    for anime_data in anime_list:
        anime_id = str(anime_data["id"])
        doc_ref = collection_ref.document(anime_id)
        batch.set(doc_ref, anime_data)

    batch.commit()


def clear_out_collection(collection_ref):
    batch_size = 500
    while True:
        docs = collection_ref.limit(batch_size).stream()  # Fetch a batch of documents
        deleted = 0

        batch = db.batch()

        for doc in docs:
            batch.delete(doc.reference)  # Add each document to the batch
            deleted += 1

        if deleted == 0:
            break

        batch.commit()


def clear_out_users():
    batch_size = 500
    collection_ref = db.collection("User")

    while True:
        docs = collection_ref.limit(batch_size).stream()  # Fetch a batch of documents
        deleted = 0

        batch = db.batch()

        for doc in docs:
            batch.delete(doc.reference)  # Add each document to the batch
            deleted += 1

        if deleted == 0:
            break

        batch.commit()


def _convert_user_data(user_data: DocumentSnapshot) -> User:
    """Converts a user data document to an User object."""
    user_dict = user_data.to_dict()
    user = User(
        pfp=user_dict.get('pfp'),
        name=user_dict.get('name'),
        completed=user_dict.get('completed'),
        unique=user_dict.get('unique')
    )
    return user


def get_user_data(user_name: str | None = None) -> User | dict[str, User]:
    """Gets user data from Firebase.
    If user_name is None, returns all user data, else only a specific user.
    """
    users_data = {}
    if user_name:
        user_docs = db.collection("User").where(filter=FieldFilter('name', '==', user_name)).get()
        if len(user_docs) != 1:
            raise ValueError(f'User name {user_name} not found!')
        users_data = _convert_user_data(user_docs[0])
    else:
        user_collection = db.collection("User")
        for user_doc in user_collection.stream():
            user = _convert_user_data(user_doc)
            users_data.update({user.name: user})
    return users_data


def _convert_anime_data(anime_data: DocumentSnapshot) -> Anime:
    """Converts a anime data document to an Anime object."""
    data_dict = anime_data.to_dict()
    anime = Anime(
        id=data_dict.get('id'),
        title=data_dict.get('title'),
        media=data_dict.get('media'),
        picture=data_dict.get('picture'),
        rating=data_dict.get('rating'),
        episodes=data_dict.get('episodes'),
        episode_duration=data_dict.get('episode_duration'),
    )
    return anime


def get_user_anime_data(user_name: str | None = None) -> list[Anime] | dict[str, list[Anime]]:
    """Gets user unique anime data from Firebase.
    If user_name is None, returns all users anime data, else only a specific user.
    """
    users_uniques = {}
    if user_name:
        unique_docs = db.collection("Anime").document(user_name).collection("Uniques").stream()
        users_uniques = [_convert_anime_data(doc) for doc in unique_docs]
    else:
        anime_ref = db.collection("Anime")
        users = anime_ref.list_documents()
        for user in users:
            unique_collection = user.collection("Uniques")
            user_unique_animes = [_convert_anime_data(doc) for doc in unique_collection.stream()]
            users_uniques.update({user.id: user_unique_animes})
    return users_uniques

def update_last_updated():
    doc_ref = db.collection('UploadDate').document('upload_date')
    doc_ref.set({'timestamp': firestore.SERVER_TIMESTAMP})


def get_anime_cache():
    cache = {}
    for doc in db.collection("AnimeCache").stream():
        cache[doc.id] = doc.to_dict()
    return cache


def upload_anime_cache(anime_list):
    if not anime_list:
        return
    collection_ref = db.collection("AnimeCache")
    batch = db.batch()
    count = 0
    for anime_data in anime_list:
        doc_ref = collection_ref.document(str(anime_data["id"]))
        batch.set(doc_ref, anime_data)
        count += 1
        if count % 500 == 0:
            batch.commit()
            batch = db.batch()
    if count % 500 != 0:
        batch.commit()
