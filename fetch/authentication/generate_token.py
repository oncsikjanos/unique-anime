"""One-time interactive script to bootstrap a fresh MyAnimeList token.

Run this locally when the token chain has fully expired and needs re-seeding:

    cd fetch
    export MAL_CLIENT_SECRET=...        # or you'll be prompted
    python -m authentication.generate_token

It prints an authorize URL, you log in + approve in the browser, paste back the
redirect URL (or just the `code` param), and it prints the full token JSON to
copy into the GitHub `MAL_TOKEN` secret.
"""
import getpass
import json
import random
import secrets
import string
from urllib.parse import urlencode, urlparse, parse_qs

import requests

from authentication import auth


def generate_code_verifier():
    length = random.randint(43, 128)
    characters = string.ascii_letters + string.digits + "-._~"
    return ''.join(secrets.choice(characters) for _ in range(length))


def main():
    client_secret = auth.CLIENT_SECRET or getpass.getpass('MAL client secret: ').strip()
    if not client_secret:
        raise SystemExit('A client secret is required.')

    # MAL supports the PKCE "plain" method, so the challenge equals the verifier.
    code_verifier = generate_code_verifier()
    params = {'response_type': 'code',
              'client_id': auth.CLIENT_ID,
              'code_challenge': code_verifier,
              'code_challenge_method': 'plain'}
    authorize_url = f"https://myanimelist.net/v1/oauth2/authorize?{urlencode(params)}"

    print("\n1) Open this URL in your browser, log in and approve:\n")
    print(authorize_url)
    print("\n2) You will be redirected to your redirect URI. Copy the full")
    print("   redirect URL (or just the value of the `code` query param).\n")

    raw = input("Paste redirect URL or code: ").strip()
    code = parse_qs(urlparse(raw).query).get('code', [raw])[0]

    payload = {'client_id': auth.CLIENT_ID,
               'client_secret': client_secret,
               'grant_type': 'authorization_code',
               'code': code,
               'code_verifier': code_verifier}
    response = requests.post(auth.TOKEN_URL, data=payload, timeout=30)
    response.raise_for_status()
    token = response.json()

    print("\nSuccess. Copy the JSON below into the GitHub `MAL_TOKEN` secret:\n")
    print(json.dumps(token, indent=4))


if __name__ == "__main__":
    main()
