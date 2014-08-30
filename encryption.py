import hashlib
import sys

__author__ = 'k'
"""
This is a set of function to be used by both client & server in order to establish a symmetric encryption
between them (encryption + auth)
"""
from Crypto.Cipher import AES

def lazysecret(secret, blocksize=32, padding='}'):
    """pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding
    return secret

def encrypt(plaintext, secret, lazy=True):
    """encrypt plaintext with secret
    plaintext   - content to encrypt
    secret      - secret to encrypt plaintext
    lazy        - pad secret if less than legal blocksize (default: True)
    checksum    - attach sha1 byte encoded (default: True)
    returns ciphertext
    """
    secret = lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)
    output = (encobj.encrypt(plaintext), hashlib.sha1.hexdigest(plaintext))  # (encrypted,hash)
    return output

def decrypt(ciphertext, secret, lazy=True):
    """decrypt ciphertext with secret
    ciphertext  - encrypted content to decrypt
    secret      - secret to decrypt ciphertext
    lazy        - pad secret if less than legal blocksize (default: True)
    checksum    - verify crc32 byte encoded checksum (default: True)
    returns plaintext
    """
    secret = lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)
    data = ciphertext[0]
    auth = ciphertext[1]
    plaintext = encobj.decrypt(ciphertext)
    if hashlib.sha1.hexdigest(data) != auth:
        print "hash mismatch"
        sys.exit()
    return plaintext