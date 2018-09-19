"""
    app.helpers
    ~~~~~~~~~~~
"""
from hashlib import sha256, md5


def register_user(User, email, first_name, last_name, password):
    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.set_default_username()
    user.commit()
    return user


def hash_list(hash_list, hash_type='md5'):
    string = '_'.join(map(str, hash_list)).encode('UTF-8')
    digest = md5(string) if hash_type == 'md5' else sha256(string)
    return digest.hexdigest()
