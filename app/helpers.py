"""
    app.helpers
    ~~~~~~~~~~~
"""
from hashlib import sha256, md5


def hash_list(hash_list, hash_type='md5'):
    string = '_'.join(map(str, hash_list)).encode('UTF-8')
    digest = md5(string) if hash_type == 'md5' else sha256(string)
    return digest.hexdigest()
