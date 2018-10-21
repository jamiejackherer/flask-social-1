"""
    app.helpers
    ~~~~~~~~~~~
"""
import os
from hashlib import sha256, md5
from urllib.parse import urlparse, ParseResult
from flask import current_app
from PIL import Image, ImageOps


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class ProfilePictureHelper:
    def __init__(self, user):
        self.user_id = user.id

    @property
    def filename(self):
        return hash_list([self.user_id])
    
    def resize_image(self, size):
        img = Image.open(self.filename)
        method = Image.NEAREST if img.size == size else Image.ANTIALIAS
        return ImageOps.fit(img, size, method=method)

    def create_image(self):
        pass

    def save(self, filename):
        user_dir = current_app.config['USER_DIR']
        if not os.path.isdir(user_dir):
            os.makedirs(user_dir)


def register_user(User, email, first_name, last_name, password):
    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.set_default_username()
    user.commit()
    return user


def hash_list(hash_list, hash_type='md5'):
    """ Concat a list of text together to make a unique hash.

        Example:
            hash_list(['one', 'two', 'three'], md5)

        :param hash_list: List of text items to be concated
        :param hash_type: Type of algorithm to hash the concated string
    """
    string = '_'.join(map(str, hash_list)).encode('UTF-8')
    if hash_type == 'md5':
        digest = md5(string)
    else:
        digest = sha256(string)
    return digest.hexdigest()


def truncate(text, max_length=150):
    """ Truncate `text` to `max_length`.

        :param text: Text to truncate
        :param max_length: Max length of text
    """
    if len(text) > max_length:
        text = '{}...'.format(text[0:max_length])
    return text


def grammar_pluralize(text, countable):
    """ Pluralize `text` if `countable` is not singular.

        :param text: Text that should be plural, or not
        :param countable: Integer to check if `text` should be plural
    """
    if countable != 1:
        text = '{}s'.format(text)
    return text


def grammar_posession(text):
    """ Grammar for posessive nouns.

        Examples:
            - John becomes John's
            - Jess becomes Jess'

        :param: Text to form a posessive
    """
    if text[-1:].lower() == 's':
        text = '{}\''.format(text)
    else:
        text = '{}\'s'.format(text)
    return text


def prepend_url(url):
    p = urlparse(url, 'http')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    p = ParseResult('http', netloc, path, *p[3:])
    return p.geturl()
