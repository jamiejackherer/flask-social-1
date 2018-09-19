from app.app import create_app
from app.extensions import db
from app.users.models import User


app = create_app()


class Test:
    def __init__(self):
        self.ono = User.query.filter_by(first_name='Daniel').first()

    def create_users(self):
        User(email='ono@testing.com', first_name='Daniel',
             last_name='Lindegren', password='testing').register()
        User(email='sheree@testing.com', first_name='Sheree',
             last_name='Score', password='testing').register()
        User(email='mike@testing.com', first_name='Mike',
             last_name='Johnson', password='testing').register()
        User(email='susan@testing.com', first_name='Susan',
             last_name='Roberts', password='testing').register()
        User(email='jennifer@testing.com', first_name='Jennifer',
             last_name='Michaels', password='testing').register()
        User(email='tammy@testing.com', first_name='Tammy',
             last_name='Fowler', password='testing').register()
        User(email='jordan@testing.com', first_name='Jordan',
             last_name='Green', password='testing').register()
        User(email='sam@testing.com', first_name='Sam',
             last_name='Jennings', password='testing').register()
        
        print('Restart the python shell before doing anything else.')


@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
        'Test': Test,
    }
