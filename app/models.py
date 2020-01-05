from app import db


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Dashboard: {}>'.format(self.id)
