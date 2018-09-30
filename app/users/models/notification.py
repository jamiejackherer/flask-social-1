"""
    app.users.models.notification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Notification model.
"""
import json
from app.extensions import db
from app.models import BaseModel


class Notification(db.Model, BaseModel):
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payload_json = db.Column(db.Text)

    def __repr__(self):
        return '<Notification {} {}>'.format(self.name, self.user_id)

    def get_data(self):
        return json.loads(str(self.payload_json))
