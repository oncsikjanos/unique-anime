import json
import requests
from requests.exceptions import HTTPError
from authentication import authCodeGenerator as authGen
import os
import logging
from urllib.parse import urlencode


def authorize():
    code_verifier = authGen.generate_code_verifier()
    params = {'response_type': 'code',
              'client_id': '82afa89d009d84b460c3f0cd41082a4a',
              'code_challenge': code_verifier,
              'code_challenge_method': 'plain'}
    url = f"https://myanimelist.net/v1/oauth2/authorize?{urlencode(params)}"
    print("Open this URL in your browser, log in, approve, then copy the 'code' query param from the redirect:")
    print(url)
    return url

# Gets the auth_token from myanimelist
def get_auth_code(auth_code):
    url = "https://myanimelist.net/v1/oauth2/token"
    payload = {'client_id': '82afa89d009d84b460c3f0cd41082a4a',
               'client_secret': '***REMOVED-MAL-CLIENT-SECRET***',
               'grant_type': 'authorization_code',
               'code': auth_code,
               'code_verifier': 'rSs6V5FS~cBqbibKmrkqchHGY9gjGz1V~1Qd_M~x4XaW5i2-OGbuIiRqSBqVSRTs1rGb~TSDBy4DOgnxLMqdFJ45MigUuqccA3hiJnQPCOBbwm1Lqr'}
    token_request = requests.post(url, data=payload)
    if token_request.status_code == 200:
        data = token_request.json()
        file_path = 'token_myanimelist.json'
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    print(token_request.text)


def get_access_token():
    token_json = os.environ.get('MAL_TOKEN_JSON')
    if not token_json:
        raise EnvironmentError('MAL_TOKEN_JSON environment variable is not set')
    return json.loads(token_json)['access_token']


def refresh_token(auth_code):
    if not os.path.isfile('authentication/token_myanimelist.json'):
        logging.warning('Cant refresh token_myanimelist.json does not exist')
        return False

    with open('token_myanimelist.json') as json_file:
        json_data = json.load(json_file)

    api_refresh_token = json_data['refresh_token']
    url = "https://myanimelist.net/v1/oauth2/token"
    payload = {'client_id': '82afa89d009d84b460c3f0cd41082a4a',
               'client_secret': '***REMOVED-MAL-CLIENT-SECRET***',
               'grant_type': 'refresh_token',
               'refresh_token': api_refresh_token,
               'code': code,
               'code_verifier': 'rSs6V5FS~cBqbibKmrkqchHGY9gjGz1V~1Qd_M~x4XaW5i2-OGbuIiRqSBqVSRTs1rGb~TSDBy4DOgnxLMqdFJ45MigUuqccA3hiJnQPCOBbwm1Lqr'
     } #authGen.get_code_verifier()}
    headers = {'Host': 'https://toxictsuniqueanime.web.app/',
               'Content-Type': 'application/x-www-form-urlencoded'}

    request = requests.post(url, data=payload, headers=headers)
    try:
        request.raise_for_status()
        data = request.json()
        file_path = 'token_myanimelist.json'
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return True
    except HTTPError as e:
        logging.warning(e)
    return False

# get_auth_code('***REMOVED-MAL-TOKEN***')