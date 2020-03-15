from flask_restful import Resource, reqparse
from flask import make_response
from resources import db
from resources.models import User, BillingPlan, UserBillingPlan
from resources.utils import DecimalEncoder
from resources.config import BILLING_PLANS
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims, current_user
from pycard import Card
from werkzeug.exceptions import BadRequest, ServiceUnavailable
import json
from time import time

class BillingResource(Resource):

    @jwt_required
    def post(self):
        '''
        change the billing plan of a user
        '''
        username = get_jwt_identity()
        is_admin = get_jwt_claims()['is_admin']
        if is_admin:
            raise BadRequest('no billing plans for administrators')

        current_time = int(time()) # number of seconds since the Epoch

        try:
            user_billing_plan = UserBillingPlan.query.filter_by(userId=current_user.Id).first()
        except:
            raise ServiceUnavailable('Database error')

        if user_billing_plan is not None:
            try:
                bp = BillingPlan.query.get(user_billing_plan.billingPlanId)
                billing_plan_name = bp.plan
                user_billing_plan_duration = bp.duration
                purchase_time = user_billing_plan.purchasedAt
            except:
                raise ServiceUnavailable('Database error')

            if billing_plan_name == 'DEV': # this plan is for dev purposes only
                billing_plan_duration = user_billing_plan_duration * 5 * 60 # 5 minutes
            else:
                billing_plan_duration = user_billing_plan_duration * 24 * 60 * 60 # in seconds

            if current_time > purchase_time + billing_plan_duration:
            	try:
            		UserBillingPlan.query.filter_by(userId=current_user.Id).delete()
            	except:
            		raise ServiceUnavailable('Database error')
            else:
                raise BadRequest(f"User '{username}' has already a billing plan of type '{billing_plan_name}'. Contact an administrator to cancel it.")

        # read card details and billing plan from POST body
        parser = reqparse.RequestParser()

        # card details
        parser.add_argument('number', type=str, required=True)
        parser.add_argument('month', type=int, required=True)
        parser.add_argument('year', type=int, required=True)
        parser.add_argument('cvc', type=int, required=True)
        parser.add_argument('holder', type=str, required=True)
        # billing plan
        parser.add_argument('plan', type=str, choices=BILLING_PLANS.keys(), required=True)

        try:
            request_details = parser.parse_args()
        except Exception as e:
            raise BadRequest('Invalid and/or missing request parameters')

        billing_plan_name = BILLING_PLANS[request_details['plan']]
        card_details = dict(request_details)
        del card_details['plan']

        try:
            card = Card(**card_details)
        except Exception as e:
            raise BadRequest('Invalid card details')

        # check validity of card using the Luhn algorithm (mod 10 validity)
        if not card.is_valid:
            raise BadRequest('Card not valid')

        ### at this point, we have a valid card and a valid billing plan ###

        try:
            billing_plan = BillingPlan.query.filter_by(plan=billing_plan_name).first()
            payment_amount = billing_plan.amount
        except:
            raise ServiceUnavailable('Database error')

        #####################################
        # processing payment, obviously...  #
        # Processing done!                  #
        # We got the money, without errors! #
        #####################################

        # create a new billing for the user
        try:
            db.session.add(
                UserBillingPlan(userId=current_user.Id, billingPlanId=billing_plan.Id, purchasedAt=current_time)
            )
            # billing is effective immediately
            current_user.max_quota = billing_plan.max_quota
            current_user.access_time = current_time - 61
            db.session.commit()
        except:
            db.session.rollback()
            raise ServiceUnavailable('Database error')

        return make_response({
            'username': username,
            'billing plan': billing_plan_name,
            'amount paid (eur)': payment_amount,
            'card number': card.mask
        })

class BillingPlansResource(Resource):

    def get(self):
        '''
        return a list of all billing plans available to users
        '''
        try:
            billingPlans = BillingPlan.query.all()
        except:
            raise ServiceUnavailable('Database error')

        billing_plan_list = [
            { column.name : str(getattr(bp, column.name)) for column in bp.__table__.columns }
            for bp in billingPlans
        ]

        response = make_response(json.dumps(billing_plan_list, cls=DecimalEncoder))
        response.headers['content-type'] = 'application/json'
        return response
