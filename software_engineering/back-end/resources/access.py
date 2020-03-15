from flask_restful import Resource
from flask import make_response, abort, request
from resources import db
from resources.utils import username_password_parser, UserView
from resources.models import User, LoggedOutTokens
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt, get_jwt_identity
from werkzeug.exceptions import BadRequest, Unauthorized, ServiceUnavailable
from time import time

class LoginResource(Resource):

    parser = username_password_parser()

    def post(self):
        '''
        Login the user, returning them their token in the form {'token': token}
        '''
        if request.content_type is None or not request.content_type.startswith('application/x-www-form-urlencoded'):
            raise BadRequest('Malformed login form')

        args = self.parser.parse_args()
        username = args['username']
        password = args['password']

        if username is None or password is None:
            missing = []
            if username is None:
                missing.append('username')
            if password is None:
                missing.append('password')
            raise BadRequest({'Obligatory fields missing': missing})

        # check that the user exists in our database
        try:
            user = User.query.filter_by(username=username).first()
        except:
            raise ServiceUnavailable('Database error')

        if user is not None:
            password_is_correct = user.is_correct_password(password)

        if user is None or not password_is_correct:
            raise Unauthorized('Wrong username and/or password')

        # checks were successful, return an access token
        return make_response({'token': create_access_token(identity=user)})

class LogoutResource(Resource):

    @jwt_required
    def post(self):
        '''
        Logout the user, returning 200 and an empty response body
        '''
        global loggedout

        raw_jwt = get_raw_jwt()
        jti = raw_jwt['jti']
        exp = raw_jwt['exp'] # JWT expiration time in seconds since the Epoch

        current_time = int(time()) # current time in seconds since the Epoch
        database_error = False

        try:
            # first remove all expired JWTs from the blacklist...
            LoggedOutTokens.query.filter(LoggedOutTokens.exp < current_time).delete(synchronize_session=False)
            # ...then add the current one
            db.session.add(LoggedOutTokens(jti=jti, exp=exp))
            db.session.commit()
        except:
            raise ServiceUnavailable('Database error')

        return '', 200

class AccountResource(UserView, Resource):

    @jwt_required
    def get(self):
        '''
        Return the account details of the current user
        '''
        return make_response(self.user_details(get_jwt_identity()))
