from app.models import *
from sqlalchemy import exc
import json


def login(userId, password):
    userList = {'test': 'test', 'user1': 'muroran1', 'user2': 'muroran2', 'user3': 'muroran3', 'user4': 'muroran4',
                'user5': 'muroran5', 'aaa': 'aaa'}
    if userId in userList and userList[userId] == password:
        return {'result': 'Success!'}, 200
    return {'result': 'Login failed'}, 400


def dashboard_get(userId):
    # get all the list of dashboard belongs to the user
    dashboards = Dashboard.query.filter_by(userId=userId).all()
    res = []
    for dashboard in dashboards:
        d = {'id': dashboard.id, 'userId': dashboard.userId}
        res.append({**d, **json.loads(dashboard.content)})
    return {'dashboards': res}, 200


def dashboard_post(userId, dashboard):
    # create new dashboard
    d = Dashboard(userId=userId, content=dashboard)
    db.session.add(d)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return {'result': str(e)}, 400
    return {'result': 'Success!'}, 200


def dashboard_put(userId, dashboard, dashboardId):
    # update dashboard
    d = Dashboard(id=int(dashboardId), userId=userId, content=dashboard)
    db.session.merge(d)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return {'result': str(e)}, 400
    return {'result': 'Success!'}, 200


def dashboard_get_single(userId, dashboardId):
    dashboard = Dashboard.query.filter_by(userId=userId, id=dashboardId).first()
    if dashboard:
        d = {'id': dashboard.id, 'userId': dashboard.userId}
        return {**d, **json.loads(dashboard.content)}, 200
    else:
        return {'result': 'Dashboard not found'}, 404


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
