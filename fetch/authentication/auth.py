import json
import os
import requests

# client_id is not secret (it is sent to the browser in the authorize URL), so a
# default is fine; client_secret must come from the environment / GitHub secret.
CLIENT_ID = os.environ.get('MAL_CLIENT_ID', '82afa89d009d84b460c3f0cd41082a4a')
CLIENT_SECRET = os.environ.get('MAL_CLIENT_SECRET')

TOKEN_URL = "https://myanimelist.net/v1/oauth2/token"
# Written by refresh_access_token() so the workflow can push the rotated token
# back into the MAL_TOKEN secret. Gitignored.
TOKEN_FILE = 'token_myanimelist.json'


def get_access_token():
    token_json = os.environ.get('MAL_TOKEN_JSON')
    if not token_json:
        raise EnvironmentError('MAL_TOKEN_JSON environment variable is not set')
    return json.loads(token_json)['access_token']


def refresh_access_token():
    """Exchange the stored refresh_token for a fresh token.

    MAL rotates the refresh_token on every call and invalidates the old one, so
    the new token is persisted both in-process (MAL_TOKEN_JSON, for this run) and
    to TOKEN_FILE (so the workflow can update the MAL_TOKEN secret for next time).
    Returns the new token dict.
    """
    if not CLIENT_SECRET:
        raise EnvironmentError('MAL_CLIENT_SECRET environment variable is not set')

    token_json = os.environ.get('MAL_TOKEN_JSON')
    if not token_json:
        raise EnvironmentError('MAL_TOKEN_JSON environment variable is not set')

    payload = {'client_id': CLIENT_ID,
               'client_secret': CLIENT_SECRET,
               'grant_type': 'refresh_token',
               'refresh_token': json.loads(token_json)['refresh_token']}

    response = requests.post(TOKEN_URL, data=payload, timeout=30)
    response.raise_for_status()
    new_token = response.json()

    os.environ['MAL_TOKEN_JSON'] = json.dumps(new_token)
    with open(TOKEN_FILE, 'w') as json_file:
        json.dump(new_token, json_file, indent=4)

    return new_token
