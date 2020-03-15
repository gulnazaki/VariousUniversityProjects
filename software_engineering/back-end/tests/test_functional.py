import pytest
from resources.config import FREE_QUOTA_PER_MINUTE
from resources.models import User, BillingPlan, UserBillingPlan
from .utils import token_header
import time

# Check each endpoint's sideffects to db
# basic scenarios

class TestAdmin(object):

    admin_data = {
        'username': 'admin',
        'password': '321nimda'
    }
    admin_token = None
    dummy_user_data = {
        'username': 'puppy',
        'password': 'isecretlyloveacat',
        'email': 'nomail@nomail.eu',
    }
    dummy_update_data = {
        'password': 'inowhateacat',
        'email': 'nomail@nomail.ca',
        'quota': FREE_QUOTA_PER_MINUTE - 1
    }

    def test_LoginResource(self, client):
        # try to login admin
        rv = client.post('energy/api/Login', data=TestAdmin.admin_data)
        assert rv.status_code == 200
        assert rv.json['token'] is not None
        TestAdmin.admin_token = rv.json['token']

    def test_AdminUserResource(self, client):
        # add a user
        rv = client.post('energy/api/Admin/users', headers=token_header(TestAdmin.admin_token), data=TestAdmin.dummy_user_data)
        assert rv.status_code == 200
        assert rv.json['new user'] == TestAdmin.dummy_user_data['username']

        # hit users list
        rv = client.get('energy/api/Admin/users', headers=token_header(TestAdmin.admin_token))
        assert rv.status_code == 200

        # verify that new user exists and her credentials are stored correctly in the db
        assert len(rv.json) > 1
        assert rv.json[-1]['username'] == TestAdmin.dummy_user_data['username']

        db_user = User.query.filter_by(username=rv.json[-1]['username']).first()
        assert db_user is not None
        assert db_user.is_correct_password(TestAdmin.dummy_user_data['password']) # -assert check for secure passwords? too much-
        assert db_user.is_admin == False
        assert db_user.email == TestAdmin.dummy_user_data['email']
        assert db_user.max_quota == FREE_QUOTA_PER_MINUTE
        assert db_user.current_quota == FREE_QUOTA_PER_MINUTE

    def test_AdminGetOrEditUserResource(self, client):
        # get dummy_user's details
        rv = client.get('energy/api/Admin/users/' + TestAdmin.dummy_user_data['username'], headers=token_header(TestAdmin.admin_token))
        assert rv.status_code == 200
        assert rv.json['username'] == TestAdmin.dummy_user_data['username']

        # update her details
        rv = client.put('energy/api/Admin/users/' + TestAdmin.dummy_user_data['username'], headers=token_header(TestAdmin.admin_token), data=TestAdmin.dummy_update_data)
        print(rv.data)
        assert rv.status_code == 200
        assert rv.json['username'] == TestAdmin.dummy_user_data['username']
        assert len(rv.json['updated fields']) == len(TestAdmin.dummy_update_data)
        db_user = User.query.filter_by(username=rv.json['username']).first()
        assert db_user is not None
        assert rv.json['updated fields']['password (hash)'] == db_user.password_hash
        assert rv.json['updated fields']['email'] == db_user.email == TestAdmin.dummy_update_data['email']
        assert rv.json['updated fields']['max quota'] == db_user.max_quota == TestAdmin.dummy_update_data['quota']

    def test_LogoutResource(self, client):
        rv = client.post('energy/api/Logout', headers=token_header(TestAdmin.admin_token))
        assert rv.status_code == 200
        TestAdmin.admin_token = None

class TestUser(object):

    user_token = None
    user_data = {'username': TestAdmin.dummy_user_data['username'],
                 'password': TestAdmin.dummy_update_data['password']}
    user_quota = TestAdmin.dummy_update_data['quota']
    user_false_data = {
        'username': 'hacker',
        'password': 'notauthorizedtousethisservice'
    }
    card_data = {
        'number' : "4444333322221111",
        'month' : 9,
        'year' : 2020,
        'cvc' : 135,
        'holder' : "Babababank",
        'plan' : 'E'
    }

    expected_billing_plan = {
        'plan': 'E',
        'max_quota': 12,
        'duration': 7,
        'amount': 4.99
    }

    def test_LoginResource(self, client):
        # fail without data
        rv = client.post('energy/api/Login')
        assert rv.status_code == 400

        # fail with wrong credentials
        rv = client.post('energy/api/Login', data=TestUser.user_false_data)
        assert rv.status_code == 401

        # fail with missing values
        rv = client.post('energy/api/Login', data={'username': TestUser.user_data['username']})
        assert rv.status_code == 400
        rv = client.post('energy/api/Login', data={'password': TestUser.user_data['password']})
        assert rv.status_code == 400

        # login succesfully with correct ones
        rv = client.post('energy/api/Login', data=TestUser.user_data)
        assert rv.status_code == 200
        assert rv.json['token'] is not None
        TestUser.user_token = rv.json['token']

    def test_BillingResource(self,client):
        # make sure max quota is updated
        db_user = User.query.filter_by(username=TestUser.user_data['username']).first()
        billing_plan = UserBillingPlan.query.filter_by(userId=db_user.Id).first()

        # check user's max quota in db is as expected and that user has no current billing plan
        assert TestUser.user_quota == db_user.max_quota
        assert billing_plan is None

        # buy plan
        rv = client.post('energy/api/Billing', data=TestUser.card_data, headers=token_header(TestUser.user_token))
        assert rv.status_code == 200

        # make sure max quota is updated according to plan
        billing = TestUser.expected_billing_plan
        user_billing_plan = UserBillingPlan.query.filter_by(userId=db_user.Id).first()
        assert user_billing_plan is not None
        billing_plan = BillingPlan.query.filter_by(Id=user_billing_plan.billingPlanId).first()
        assert db_user.max_quota == billing['max_quota'] == billing_plan.max_quota

        #make sure all details are correct
        assert billing['plan'] == billing_plan.plan
        assert billing['duration'] == billing_plan.duration
        assert billing['amount'] == billing_plan.amount

    def test_LogoutResource(self, client):
        rv = client.post('energy/api/Logout', headers=token_header(TestUser.user_token))
        assert rv.status_code == 200
        TestUser.user_token = None
