import random

def get_unblock_token() -> str:
    from hashlib import sha1
    abc = "abcdefghijklmnopqrstuvwxyz"

    len_secret_word = random.randint(3, 60)
    secret_word=""
    for i in range(1, len_secret_word+1):
        secret_word+= abc[random.randint(0, len(abc)-1)]
    return sha1(secret_word.encode('utf-8')).hexdigest()