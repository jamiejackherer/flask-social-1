from app.app import create_app
from app.extensions import db
from app.users.models import User, Post
from app.helpers import register_user


app = create_app()


class Test:
    def __init__(self):
        self.ono = User.query.filter_by(first_name='Daniel').first()
        self.sheree = User.query.filter_by(first_name='Sheree').first()
        self.mike = User.query.filter_by(first_name='Mike').first()
        self.susan = User.query.filter_by(first_name='Susan').first()
        self.jennifer = User.query.filter_by(first_name='Jennifer').first()
        self.tammy = User.query.filter_by(first_name='Tammy').first()
        self.jordan = User.query.filter_by(first_name='Jordan').first()
        self.sam = User.query.filter_by(first_name='Sam').first()

    def create_users(self):
        register_user(User, 'ono@testing.com', 'Daniel', 'Lindegren',
                      'testing')
        register_user(User, 'sheree@testing.com', 'Sheree', 'Score',
                      'testing')
        register_user(User, 'mike@johnson.com', 'Mike', 'Johnson',
                      'testing')
        register_user(User, 'susan@testing.com', 'Susan', 'Roberts',
                      'testing')
        register_user(User, 'jennifer@testing.com', 'Jennifer', 'Michaels',
                      'testing')
        register_user(User, 'tammy@testing.com', 'Tammy', 'Fowler',
                      'testing')
        register_user(User, 'jordan@testing.com', 'Jordan', 'Green',
                      'testing')
        register_user(User, 'sam@testing.com', 'Sam', 'Jennings', 'testing')
        
        print('Restart the python shell before doing anything else.')


@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
        'Test': Test,
        'Post': Post,
    }
