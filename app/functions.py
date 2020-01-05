from app.models import *
from sqlalchemy import exc


def login(userId, password):
    userList = {'test': 'test', 'pirika': 'pirika', 'test2': 'test2', 'test3': 'test3'}
    if userId in userList and userList[userId] == password:
        return {'result': 'Success!'}, 200
    return {'result': 'Login failed'}, 400


def dashboard_get(userId):
    # get all the list of dashboard belongs to the user
    dashboard = Dashboard.query.filter_by(userId=userId).all()
    return {'dashboard': dashboard}, 200


def dashboard_post(userId, dashboard):
    # create new dashboard
    d = Dashboard(userId=userId, dashboard=dashboard)
    db.session.add(d)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return {'result': e}, 400
    return {'result': 'Success!'}, 200


def dashboard_put():
    # check auth?
    # update dashboard
    return {'dashboard': {}}, 200


def csv_get():
    # check auth?
    # get all the list of dashboard belongs to the user
    return {'dashboard': {}}, 200


def csv_post():
    # check auth?
    # create new dashboard
    return {'dashboard': {}}, 200


def map_get():
    # check auth?
    # get all the list of dashboard belongs to the user
    return {'dashboard': {}}, 200


def map_post():
    # check auth?
    # create new dashboard
    return {'dashboard': {}}, 200