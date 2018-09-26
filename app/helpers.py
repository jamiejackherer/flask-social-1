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
    if hash_type == 'md5':
        digest = md5(string)
    else:
        digest = sha256(string)
    return digest.hexdigest()


def truncate(text, max_length=150):
    if len(text) > max_length:
        text = '{}...'.format(text[0:max_length])
    return text
