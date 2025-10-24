import secrets
import string
import hashlib
import base64
import random

def generate_code_verifier():
    length = random.randint(43, 128)
    characters = string.ascii_letters + string.digits + "-._~"
    verifier = ''.join(secrets.choice(characters) for _ in range(length))
    with open('../verifierCode.txt', 'w') as f:
        f.write(verifier)
    return verifier


def generate_code_challenge(code_verifier, method='S256'):
    """Generate a code challenge from a code verifier."""
    if method == 'S256':
        # Use SHA256 hashing and base64url encoding
        code_challenge = hashlib.sha256(code_verifier.encode('ascii')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode('ascii')
    elif method == 'plain':
        # Plain method just returns the verifier itself
        code_challenge = code_verifier
    else:
        raise ValueError("Invalid method. Choose either 'S256' or 'plain'.")

    return code_challenge

def get_code_verifier():
    code_verifier = ""
    with open('verifierCode.txt', 'r') as f:
        code_verifier=f.read()
    return code_verifier