#!/usr/bin/env python3
from flask import request, Blueprint
from flask_restplus import Api, Resource, fields
from app.functions import *

route = Blueprint('route', __name__)
api = Api(route)

login_post_spec = api.model('Login POST', {
    'userId': fields.String(description='UserId'),
    'password': fields.String(description='Hashed password')
})

login_post_response_spec = api.model('Login POST Response', {
    'result': fields.String(description='Result'),
})

# dashboard_get_response_spec = api.model('Dashboard GET Response', {
#     'dashboards': field.list(description='Dashboard list'),
# })

# dashboard_single_get_response_spec = api.model('Specific Dashboard GET Response', {
#     'dashboard': fields.String(description='Dashboard'),
# })

dashboard_post_spec = api.model('Dashboard POST', {
    'dashboard': fields.String(description='New dashboard')
})

dashboard_put_spec = api.model('Dashboard PUT', {
    'dashboardId': fields.String(description='Dashboard id'),
    'dashboard': fields.String(description='Update dashboard')
})

csv_get_spec = api.model('CSV GET', {
    'userId': fields.String(description='UserId'),
    'dashboardId': fields.String(description='Dashboard id'),
    'dashboard': fields.String(description='Update dashboard')
})

csv_post_spec = api.model('CSV POST', {
    'userId': fields.String(description='UserId'),
    'dashboardId': fields.String(description='Dashboard id'),
    'dashboard': fields.String(description='Update dashboard')
})

map_get_spec = api.model('MAP GET', {
    'userId': fields.String(description='UserId'),
    'dashboardId': fields.String(description='Dashboard id'),
    'dashboard': fields.String(description='Update dashboard')
})

map_post_spec = api.model('MAP POST', {
    'map': fields.String(description='Target map json string')
})


@api.route('/login')
@api.doc(
    responses={
        200: 'Success',
        400: 'Validation Error'
    })
class Login(Resource):
    @api.expect(login_post_spec)
    @api.marshal_with(login_post_response_spec)
    def post(self):
        return login(request.json['userId'], request.json['password'])


@api.route('/dashboard/<string:userId>')
class Dashboard(Resource):
    # @api.marshal_with(dashboard_get_response_spec)
    def get(self, userId):
        return dashboard_get(userId)

    @api.expect(dashboard_post_spec)
    def post(self, userId):
        return dashboard_post(userId, request.json['dashboard'])

    @api.expect(dashboard_put_spec)
    def put(self, userId):
        return dashboard_put(userId, request.json['dashboard'], request.json['dashboardId'])


@api.route('/dashboard/<string:userId>/<string:dashboardId>')
class SDashboard(Resource):
    # @api.marshal_with(dashboard_single_get_response_spec)
    def get(self, userId, dashboardId):
        return dashboard_get_single(userId, dashboardId)


@api.route('/csv')
class CSV(Resource):
    @api.expect(csv_get_spec)
    def get(self):
        return csv_get()

    @api.expect(csv_post_spec)
    def post(self):
        return csv_post()


@api.route('/map')
class MAP(Resource):
    @api.expect(map_get_spec)
    def get(self):
        return map_get()

    @api.expect(map_post_spec)
    def post(self):
        return map_post()


@api.route('/createDB')
class MAP(Resource):
    def get(self):
        db.create_all()
        return 200
