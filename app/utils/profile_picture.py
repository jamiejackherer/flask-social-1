"""
    app.utils.profile_picture
    ~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import os
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image, ImageOps
from app.helpers import hash_list


class ProfilePicture:
    def __init__(self, user, pp_data):
        self.user_id = user.id
        self.pp_data = pp_data

    def resize_image(self, filename, size):
        img = Image.open(filename)
        method = Image.NEAREST if img.size == size else Image.ANTIALIAS
        return ImageOps.fit(img, size, method=method)

    def create_image(self):
        user_dir = current_app.config['USER_DIR']
        if not os.path.isdir(user_dir):
            os.makedirs(user_dir)
        og_filename = secure_filename(self.pp_data.filename)
        og_full_path = '{}/{}'.format(user_dir, og_filename)
        self.pp_data.save(og_full_path)

        basename = hash_list([self.user_id])
        full_path = '{}/{}.jpg'.format(user_dir, basename)
        img = self.resize_image(og_full_path, (160, 160))
        img.save(full_path, 'JPEG', quality=95)

        if os.path.exists(og_full_path):
            os.remove(og_full_path)

        return basename
