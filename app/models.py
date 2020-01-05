from app import db
import datetime


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(255))
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Dashboard: {}>'.format(self.id)
