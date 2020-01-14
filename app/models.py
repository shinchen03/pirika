from app import db
import json


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)

    def __repr__(self):
        try:
            content = json.loads(self.content)
        except ValueError:
            content = self.content
        return '<DashboardId: {}, UserId: {}, Content: {}>'.format(self.id, self.userId, content)
