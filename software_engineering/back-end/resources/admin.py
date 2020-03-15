from flask_restful import Resource
from flask import make_response, request
from resources.utils import username_password_parser, DecimalEncoder
from werkzeug.exceptions import BadRequest, ServiceUnavailable, Forbidden as NoData, Unauthorized
from resources import db
from resources.models import (
    User,
    BillingPlan,
    UserBillingPlan,
    ActualTotalLoad,
    AggregatedGenerationPerType,
    DayAheadTotalLoadForecast,
)
from resources.utils import UserView
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from io import TextIOWrapper
import pandas as pd
from functools import wraps
import json
import time

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['is_admin']:
            raise Unauthorized('administrators only')
        else:
            return fn(*args, **kwargs)
    return wrapper

class AdminUserResource(UserView, Resource):

    parser = username_password_parser()

    @admin_required
    def get(self):
        '''
        return a list of all users with details about them
        '''
        try:
            users = User.query.all()
        except:
            raise ServiceUnavailable('Database error')

        user_list = [self.user_details(user.username) for user in users]

        response = make_response(json.dumps(user_list, cls=DecimalEncoder))
        response.headers['content-type'] = 'application/json'
        return response

    @admin_required
    def post(self):
        '''
        add a new user
        body of request should contain:
        - "username" (string, required always)
        - "password" (string, required here)
        - "email" (string, required here)
        - "is_admin" (bool, default: False)
        - "max_quota" (int, default: free-rider value)
        '''
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']
        is_admin = args['is_admin']
        max_quota = args['quota']

        if username is None: raise BadRequest(f'A username should be provided for this request')
        if password is None: raise BadRequest(f'A password should be provided for this request')
        if email is None:    raise BadRequest(f'An email should be provided for this request')

        try:
            # check if user exists
            user = User.query.filter_by(username=username).first()
        except:
            raise ServiceUnavailable('Database error')

        if user is not None:
            raise BadRequest(f"User '{username}' already exists")

        try:
            # if not, add the new user
            db.session.add(
                User(username=username, password=password, is_admin=is_admin, email=email, max_quota=max_quota, current_quota=max_quota, access_time=int(time.time()))
            )
            db.session.commit()

        except:
            db.session.rollback()
            raise ServiceUnavailable('Database error')

        return make_response({'new user': username, 'status': 'successfully added'})

class AdminGetOrEditUserResource(UserView, Resource):

    parser = username_password_parser()

    @admin_required
    def get(self, username):
        '''
        return details of the user with username <username>
        '''
        return make_response(self.user_details(username))

    @admin_required
    def put(self, username):
        '''
        edit data regarding the user with username "username"
        body of request should contain:
        - "password" (string, optional)
        - "email" (string, optional)
        - "is_admin" (bool, optional)
        - "quota" (int, optional)
        '''
        args = self.parser.parse_args()
        password = args['password']
        email = args['email']
        is_admin = args['is_admin']
        quota = args['quota']

        try:
            # check if user exists
            user = User.query.filter_by(username=username).first()

            # update user fields
            updated_fields = {}

            if password is not None:
                user.password = password
                updated_fields['password (hash)'] = user.password_hash.decode('ascii')
            if email is not None:
                user.email = email
                updated_fields['email'] = email
            if is_admin is not None:
                user.is_admin = is_admin
                updated_fields['is_admin'] = is_admin
            if quota is not None:
                user.max_quota = quota
                updated_fields['max quota'] = quota
            db.session.commit()
        except:
            db.session.rollback()
            raise ServiceUnavailable('Database error')

        return make_response({'username': username, 'updated fields': updated_fields})

    @admin_required
    def delete(self, username):
        '''
        deletes the user with username <username>
        '''

        # check that the user exists
        try:
            user = User.query.filter_by(username=username).first()
        except:
            raise ServiceUnavailable('Database error')

        if user is None:
            raise BadRequest(f"User '{username}' does not exist")

        # if user exists, delete them
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            raise ServiceUnavailable('Database error')

        return '', 200

class AdminUploadCSVResource(Resource):

    @admin_required
    def post(self, dataset):
        '''
        upload a CSV file with data and import them to the database (to the appropriate dataset)
        '''
        if request.content_type is None or not request.content_type.startswith('multipart/form-data'):
            raise BadRequest('CSV file not provided')

        csv_file = request.files.get('file')

        if not csv_file:
            raise BadRequest('CSV file not provided')

        csv_file = TextIOWrapper(csv_file, encoding='utf-8')

        # TODO: read REAL C(omma)S(eparated)V(alues)
        data = pd.read_csv(csv_file, sep=r';')

        # change (pandas) NaN to (python) None
        data = data.where((pd.notnull(data)), None)

        dataset_to_update = eval(dataset)

        try:
            previous_rows_in_table = db.session.query(dataset_to_update).count()
            data.to_sql(name=dataset_to_update.__tablename__, con=db.engine, if_exists='append', index=False)
            db.session.commit()

        except:
            pass

        finally:
            totalRecordsInDatabase = db.session.query(dataset_to_update).count()
            totalRecordsInFile = len(data.index)
            totalRecordsImported = totalRecordsInDatabase - previous_rows_in_table

        return make_response({
            'totalRecordsInFile': totalRecordsInFile,
            'totalRecordsImported': totalRecordsImported,
            'totalRecordsInDatabase': totalRecordsInDatabase
        })
