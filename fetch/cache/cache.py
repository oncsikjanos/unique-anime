#from authentication import authCodeGenerator as ac
import os
#import firestore

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CACHED_USER_FILE = os.path.join(DIR_PATH, 'cache.json')

def get_users_cache():
    if os.path.isfile(CACHED_USER_FILE):
        print("getting users cache")
