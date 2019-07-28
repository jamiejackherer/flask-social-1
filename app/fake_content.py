"""
    app.fake_content
    ~~~~~~~~~~~~~~~~

    Create default/fake user content.
"""
from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app.extensions import db
from app.users.models.user import User
from app.users.models.posts import Post


class FakeContent:
    default_users = [
        ('Daniel', 'Lindegren'),
        ('Sheree', 'Score'),
        ('Mike', 'Johnson'),
        ('Susan', 'Roberts'),
        ('Jennifer', 'Michaels'),
        ('Tammy', 'Fowler'),
        ('Jordan', 'Smith'),
        ('Sam', 'Jennings')
        ]

    def __init__(self):
        self.fake = Faker()
        user_count = 0
        for first, last in self.default_users:
            user = User.query.filter_by(first_name=first).first()
            if user:
                user_count += 1
                setattr(self, first.lower(), user)
        if not user_count:
            print('*** Warning: No default users. Use :meth:`create_users`.')

    def create_users(self, count=100):
        queue = []
        # First build a list of specific users.
        for first, last in self.default_users:
            u = self._create_users(first, last, first.lower())
            queue.append(u)
        # Second build a list of random users.
        i = 0
        while i < count:
            u = self._create_users()
            queue.append(u)
            i += 1
        for r in queue:
            user = User(**r)
            user.set_password('testing')
            db.session.add(user)
            t = (r.get('first_name'), r.get('last_name'))
            if t in self.default_users:
                setattr(self, user.first_name.lower(), user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def _create_users(self, first_name=None, last_name=None, username=None):
        if not first_name:
            first_name = self.fake.first_name()
        if not last_name:
            last_name = self.fake.last_name()
        if not username:
            username = self.fake.user_name()
        return {'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': self.fake.email(),
                'bio': self.fake.text(),
                'location': '{}, {}'.format(self.fake.city(),
                                            self.fake.state()),
                'created': self.fake.past_date(start_date='-900d')}

    def create_posts(self, count=100):
        user_count = User.query.count()
        for i in range(count):
            author = User.query.offset(randint(0, user_count - 1)).first()
            if randint(0, 1):
                recipient = author
            else:
                recipient = User.query.offset(
                    randint(0, user_count - 1)).first()
            post = Post(body=self.fake.text(), author=author,
                        recipient=recipient, created=self.fake.past_date())
            post.commit()

    def drop_tables(self):
        db.drop_all()
        db.session.commit()
