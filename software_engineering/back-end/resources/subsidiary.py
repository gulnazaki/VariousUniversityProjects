from flask_restful import Resource
from flask import make_response
from resources import db
from resources.models import (
    ActualTotalLoad,
    AggregatedGenerationPerType,
    DayAheadTotalLoadForecast,
    User,
    UserBillingPlan
)
from werkzeug.exceptions import BadRequest, ServiceUnavailable
from time import time

class HealthCheckResource(Resource):

    def get(self):
        '''
        Checks end-to-end connectivity with database
        '''
        try:
            db.session.query('1').from_statement(db.text('SELECT 1')).all()
        except:
            raise ServiceUnavailable('Database error')

        return make_response({'status': 'OK'})

class ResetResource(Resource):

    main_tables = [ActualTotalLoad, AggregatedGenerationPerType, DayAheadTotalLoadForecast, User, UserBillingPlan]

    def post(self):
        '''
        Resets the database except for the default admin account and the reference tables
        '''
        try:
            # clear & create data tables and user table only
            db.metadata.drop_all(
                db.engine,
                tables=map(lambda x : x.__table__, self.main_tables)
            )
            db.metadata.create_all(
                db.engine,
                tables=map(lambda x : x.__table__, self.main_tables)
            )

            # add default admin user
            db.session.add(User(username='admin', password='321nimda', is_admin=True, email='admin@electra.gr', access_time=int(time())))
            db.session.commit()

        except:
            db.session.rollback()
            raise ServiceUnavailable('Database error')

        return make_response({'status': 'OK'})

class HardResetResource(Resource):

    def post(self):
        '''
        COMPLETELY resets the database (!!!WARNING!!!)
        '''
        try:
            db.drop_all()
            db.create_all()
            # add default admin user
            db.session.add(User(username='admin', password='321nimda', is_admin=True, email='admin@electra.gr', access_time=int(time())))
            db.session.commit()
        except:
            db.session.rollback()
            raise ServiceUnavailable('Database error')

        return make_response({'status': 'OK'})

class ContactResource(Resource):

    def get(self):
        '''
        get the list of admin emails (for contact purposes)
        '''
        try:
            admins = User.query.filter_by(is_admin=True).all()
            admin_emails = [admin.email for admin in admins]
        except:
            raise ServiceUnavailable('Database error')
        return make_response({'admin emails': admin_emails})
