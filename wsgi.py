"""
    wsgi
    ~~~~

    Callable for uwsgi server - load production configuration.
"""
import config
from app.app import create_app


app = create_app(config.ProductionConfig)
