from flask_restful import reqparse
from flask_restful.inputs import boolean
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import HTTPException, BadRequest, ServiceUnavailable, Forbidden as NoData
from resources import db
from resources.models import *
from resources.config import FREE_QUOTA_PER_MINUTE
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt_claims, current_user
from functools import wraps
import time
import json
from decimal import Decimal

# custom handling of decimal values for json results
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

# custom "Out Of Quota" HTTP response
class OutOfQuota(HTTPException):
    code = 402
    name = 'Out Of Quota'
    description = 'Out of quota'

def reset_quota_if_necessary(user):
    current_time = int(time.time()) # seconds since the Epoch

    # first of all, check if user has a billing plan
    try:
        user_billing_plan = UserBillingPlan.query.filter_by(userId=user.Id).join(BillingPlan). \
        filter(UserBillingPlan.billingPlanId == BillingPlan.Id).first()
    except:
        raise ServiceUnavailable('Database error')
    if user_billing_plan is not None:
        # check if this plan has expired
        billing_plan_purchase_time = user_billing_plan.purchasedAt
        user_billing_plan_name = user_billing_plan.BillingPlan.plan
        user_billing_plan_duration = user_billing_plan.BillingPlan.duration

        if user_billing_plan_name == 'DEV': # this plan is for dev purposes only
            billing_plan_duration = user_billing_plan_duration * 5 * 60 # 5 minutes
        else:
            billing_plan_duration = user_billing_plan_duration * 24 * 60 * 60 # in seconds

        # billing plan has expired, do what you must
        if current_time > billing_plan_purchase_time + billing_plan_duration:
            try:
                user.max_quota = FREE_QUOTA_PER_MINUTE
                user.current_quota = min(user.current_quota, user.max_quota)
                UserBillingPlan.query.filter_by(userId=user.Id).delete()
                db.session.commit()
            except:
                db.session.rollback()
                raise ServiceUnavailable('Database error')
    # if no user billing plan exists in the database, make sure they are of type F(ree)
    else:
        try:
            #user.max_quota = FREE_QUOTA_PER_MINUTE
            user.current_quota = min(user.current_quota, user.max_quota)
            db.session.commit()
        except:
            db.session.rollback()
            raise ServiceUnavailable('Database error')

    ### done with user billing plan, proceed normally ###
    user_current_quota = user.current_quota
    user_max_quota = user.max_quota
    user_access_time = user.access_time

    # enough time has passed; we can refresh the user quota
    if current_time > user_access_time + 60:
        try:
            user.current_quota = user_max_quota
            user.access_time = current_time
            db.session.commit()
        except:
            db.session.rollback()
            raise ServiceUnavailable('Database error')

# a decorator for limit access to data endpoints (i.e. implementation of user quota)
def limited_access(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        # admins do not have quota
        is_admin = get_jwt_claims()['is_admin']
        if is_admin:
            return fn(*args, **kwargs)

        ### at this point we have a valid non-admin user (current_user) ###
        reset_quota_if_necessary(current_user)

        user_current_quota = current_user.current_quota
        user_max_quota = current_user.max_quota

        # Case 0: user is A+++
        if user_max_quota == -1:
            # no checks here, user pays a lot
            return fn(*args, **kwargs)

        # Case 1: user has quota left
        if user_current_quota > 0:
            try:
                current_user.current_quota = user_current_quota - 1
                db.session.commit()
            except:
                db.session.rollback()
                raise ServiceUnavailable('Database error')
            return fn(*args, **kwargs)

        # Case 2: user has no quota left
        if user_current_quota == 0:
            raise OutOfQuota()

    return wrapper

def username_password_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, default=None)
    parser.add_argument('password', type=str, default=None)
    parser.add_argument('email', type=str, default=None)
    parser.add_argument('is_admin', type=boolean, default=None)
    parser.add_argument('quota', type=int, default=None)
    return parser

class UserView:

    def user_details(self, username):
        try:
            user = User.query.filter_by(username=username).first()
        except:
            raise ServiceUnavailable('Database error')

        if user is None:
            raise BadRequest(f"User with username '{username}' does not exist")

        try:
            user_billing_plan = UserBillingPlan.query.filter_by(userId=user.Id).first()
            if user_billing_plan is not None:
                billing_plan = BillingPlan.query.get(user_billing_plan.billingPlanId)
                user_billing_plan_expires_at = user_billing_plan.purchasedAt + billing_plan.duration * 24 * 60 * 60
        except:
            raise ServiceUnavailable('Database error')

        reset_quota_if_necessary(user)

        response_dict = {
            'username': username,
            'password hash': user.password_hash,
            'is_admin': user.is_admin,
            'max quota': user.max_quota,
            'current quota': user.current_quota,
            'email': user.email,
        }

        if user_billing_plan is not None:
            response_dict['billing plan'] = billing_plan.plan
            response_dict['billing plan expires at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user_billing_plan_expires_at))
        else:
            response_dict['billing plan'] = 'F(ree)'

        return response_dict

class DatasetConverter(BaseConverter):

    datasets = ['ActualTotalLoad', 'AggregatedGenerationPerType', 'DayAheadTotalLoadForecast']

    def to_python(self, value):
        if value not in self.datasets:
            raise BadRequest(f'Unknown dataset: {value}')
        return value

    def to_url(self, value):
        return value

class ResolutionConverter(BaseConverter):

    resolutions = ['PT15M', 'PT30M', 'PT60M']

    def to_python(self, value):
        if value not in self.resolutions:
            raise BadRequest(f'Unknown resolution code: {value}')
        return value

    def to_url(self, value):
        return value

class DateConverter(BaseConverter):

    def to_python(self, value):
        try:
            time.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise BadRequest(f'Unknown date: {value}')
        return value

    def to_url(self, value):
        return value

class MonthConverter(BaseConverter):

    def to_python(self, value):
        try:
            time.strptime(value, "%Y-%m")
        except ValueError:
            raise BadRequest(f'Unknown month: {value}')
        return value

    def to_url(self, value):
        return value

class YearConverter(BaseConverter):

    def to_python(self, value):
        try:
            time.strptime(value, "%Y")
        except ValueError:
            raise BadRequest(f'Unknown year: {value}')
        return value

    def to_url(self, value):
        return value
