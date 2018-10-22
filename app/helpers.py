"""
    app.helpers
    ~~~~~~~~~~~
"""
import os
from datetime import datetime
from hashlib import sha256, md5
from urllib.parse import urlparse, ParseResult
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image, ImageOps


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class ProfilePhoto:
    """ Manage user profile photo files.

    - Make sure static img user directory exists.
    - Query :class:`User` to see if the user has a profile picture. If they do,
        remove that file from disk.
    - Save the image the user uploaded to disk.
    - Resize the image the user uploaded, rename it by hashing the user's
        ID and the current time, and save it to disk.
    - Remove the image the user uploaded from disk.

    :NOTE: The new hashed name is added to the user table from the view
        function this is called from.
    """
    def __init__(self, user, pp_data):
        """ Instantiate and set up variables.

        :param user: User model of :class:`User`
        :param pp_data: Data from form submission
            ``form.profile_picture.data``
        """
        self.user = user
        self.pp_data = pp_data
        self.user_dir = current_app.config['STATIC_IMG_USER_DIR']
        # Create a new filename by hashing user's ID and the current time.
        self.new_basename = hash_list([user.id, datetime.utcnow()])

    def manage_files(self):
        # Make sure ``self.user_dir`` exists before saving any files into it.
        if not os.path.isdir(self.user_dir):
            os.makedirs(self.user_dir)

        # Remove old use.
        profile_photo = self.user.profile_photo
        if profile_photo:
            full_path = self.get_full_path(profile_photo)
            self.remove_photo(full_path)

        # Save the file the user uploaded.
        up_filename = secure_filename(self.pp_data.filename)
        up_full_path = self.get_full_path(up_filename, False)
        self.pp_data.save(up_full_path)

        # Resize the file the user uploaded, and save it with the new name
        # from ``self.new_basename``.
        full_path = self.get_full_path(self.new_basename)
        img = self.resize(up_full_path, (160, 160))
        img.save(full_path, 'JPEG', quality=95)

        # Remove the file the user uploaded.
        self.remove_photo(up_full_path)

    def resize(self, full_path, size):
        img = Image.open(full_path)
        method = Image.NEAREST if img.size == size else Image.ANTIALIAS
        return ImageOps.fit(img, size, method=method)

    def remove_photo(self, full_path):
        if os.path.exists(full_path):
            os.remove(full_path)

    def get_full_path(self, basename, ext=True):
        full_path = '{}/{}'.format(self.user_dir, basename)
        if ext:
            full_path = '{}.jpg'.format(full_path)
        return full_path


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
