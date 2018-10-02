import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from app.app import create_app
from app.extensions import db
from app.users.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config.TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(username='tammy')
        user.set_password('dog')
        self.assertFalse(user.check_password('cat'))
        self.assertTrue(user.check_password('dog'))


if __name__ == '__main__':
    unittest.main()
