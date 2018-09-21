"""
    app.models
    ~~~~~~~~~~
"""
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from app.extensions import db


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    deleted = db.Column(db.DateTime)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def commit(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as E:
            db.session.rollback()
            raise E

    def delete(self):
        self.active = False
        self.deleted = datetime.utcnow()
