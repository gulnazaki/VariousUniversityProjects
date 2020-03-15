import pytest
from resources.config import FREE_QUOTA_PER_MINUTE
from resources.models import User
from .utils import token_header
import time

# Testing api's endpoints:
# to be executed with the specified order

def test_HealthCheckResource(client):
    # check db connection
    rv = client.get('energy/api/HealthCheck')
    assert rv.status_code == 200
    assert rv.json['status'] == 'OK'

class TestAdmin(object):

    admin_data = {
        'username': 'admin',
        'password': '321nimda'
    }
    admin_false_data = {
        'username': 'admin',
        'password': 'hackpassword'
    }
    admin_token = None
    dummy_user_data = {
        'username': 'boss',
        'password': 'ilovemyemployees',
        'email': 'nomail@nomail.eu',
        'is_admin': True
    }
    dummy_update_data = {
        'password': 'inowhatethem',
        'email': 'nomail@nomail.gr',
        'is_admin': False,
        'quota': FREE_QUOTA_PER_MINUTE - 1
    }
    source = {
        'ActualTotalLoad': 'dummy1.csv',
        'AggregatedGenerationPerType': 'dummy2.csv',
        'DayAheadTotalLoadForecast': 'dummy3.csv'
    }
    card_data = {
        'number' : 444333222111,
        'month' : 9,
        'year' : 2023,
        'cvc' : 666,
        'holder' : "Bababank",
        'plan' : "C"
    }

    def test_LoginResource(self, client):
        # fail without data
        rv = client.post('energy/api/Login')
        assert rv.status_code == 400

        # fail with wrong credentials
        rv = client.post('energy/api/Login', data=TestAdmin.admin_false_data)
        assert rv.status_code == 401

        # fail with missing values
        rv = client.post('energy/api/Login', data={'username': TestAdmin.admin_data['username']})
        assert rv.status_code == 400
        rv = client.post('energy/api/Login', data={'password': TestAdmin.admin_data['password']})
        assert rv.status_code == 400

        # login succesfully with correct ones
        rv = client.post('energy/api/Login', data=TestAdmin.admin_data)
        assert rv.status_code == 200
        assert rv.json['token'] is not None
        TestAdmin.admin_token = rv.json['token']

    def test_AdminUserResource(self, client):
        # you shall not pass without (valid) admin token
        rv = client.get('energy/api/Admin/users')
        assert rv.status_code == 401
        rv = client.get('energy/api/Admin/users', headers=token_header('false.token.hack'))
        assert rv.status_code == 422
        rv = client.post('energy/api/Admin/users', data=TestAdmin.dummy_user_data)
        assert rv.status_code == 401
        rv = client.post('energy/api/Admin/users', headers=token_header('false.token.hack'), data=TestAdmin.dummy_user_data)
        assert rv.status_code == 422

        # fail to add a user without data
        rv = client.post('energy/api/Admin/users', headers=token_header(TestAdmin.admin_token))
        assert rv.status_code == 400

        # fail to add a user without username/password provided
        rv = client.post('energy/api/Admin/users', headers=token_header(TestAdmin.admin_token), data={k: TestAdmin.dummy_user_data[k] for k in ['username', 'email', 'is_admin']})
        assert rv.status_code == 400
        rv = client.post('energy/api/Admin/users', headers=token_header(TestAdmin.admin_token), data={k: TestAdmin.dummy_user_data[k] for k in ['password', 'email', 'is_admin']})
        assert rv.status_code == 400
        rv = client.post('energy/api/Admin/users', headers=token_header(TestAdmin.admin_token), data={k: TestAdmin.dummy_user_data[k] for k in ['email', 'is_admin']})
        assert rv.status_code == 400

        # add a user
        rv = client.post('energy/api/Admin/users', headers=token_header(TestAdmin.admin_token), data=TestAdmin.dummy_user_data)
        assert rv.status_code == 200
        assert rv.json['new user'] == TestAdmin.dummy_user_data['username']

        # hit users list
        rv = client.get('energy/api/Admin/users', headers=token_header(TestAdmin.admin_token))
        assert rv.status_code == 200
        assert len(rv.json) > 1

        # check admin's credentials
        assert rv.json[0]['username'] == TestAdmin.admin_data['username']
        assert rv.json[0]['password hash'] is not None
        assert rv.json[0]['is_admin']
        assert rv.json[0]['max quota'] == rv.json[0]['current quota'] == FREE_QUOTA_PER_MINUTE # default value - no quota spend
        assert rv.json[0]['email'] == 'admin@electra.gr'

        # check dummy_user's credentials
        assert rv.json[-1]['username'] == TestAdmin.dummy_user_data['username']
        assert rv.json[-1]['password hash'] is not None
        assert rv.json[-1]['is_admin'] == TestAdmin.dummy_user_data['is_admin']
        assert rv.json[-1]['max quota'] == rv.json[-1]['current quota'] == FREE_QUOTA_PER_MINUTE # default value - no quota spend
        assert rv.json[-1]['email'] == TestAdmin.dummy_user_data['email']

    def test_AdminGetOrEditUserResource(self, client):
        # you shall not pass without (valid) admin token
        rv = client.get('energy/api/Admin/users/' + TestAdmin.dummy_user_data['username'])
        assert rv.status_code == 401
        rv = client.get('energy/api/Admin/users/' + TestAdmin.dummy_user_data['username'], headers=token_header('false.token.hack'))
        assert rv.status_code == 422
        rv = client.put('energy/api/Admin/users/' + TestAdmin.dummy_user_data['username'], data=TestAdmin.dummy_update_data)
        assert rv.status_code == 401
        rv = client.put('energy/api/Admin/users/' + TestAdmin.dummy_user_data['username'], headers=token_header('false.token.hack'), data=TestAdmin.dummy_update_data)
        assert rv.status_code == 422

        # get dummy_user's details
        rv = client.get('energy/api/Admin/users/' + TestAdmin.dummy_user_data['username'], headers=token_header(TestAdmin.admin_token))
        assert rv.status_code == 200
        assert rv.json['username'] == TestAdmin.dummy_user_data['username']
        assert rv.json['password hash'] is not None
        assert rv.json['is_admin'] == TestAdmin.dummy_user_data['is_admin']
        assert rv.json['max quota'] == rv.json['current quota'] == FREE_QUOTA_PER_MINUTE # default value - no quota spend
        assert rv.json['email'] == TestAdmin.dummy_user_data['email']

        # update her details
        rv = client.put('energy/api/Admin/users/' + TestAdmin.dummy_user_data['username'], headers=token_header(TestAdmin.admin_token), data=TestAdmin.dummy_update_data)
        assert rv.status_code == 200
        assert rv.json['username'] == TestAdmin.dummy_user_data['username']
        assert len(rv.json['updated fields']) == len(TestAdmin.dummy_update_data)
        assert rv.json['updated fields']['password (hash)'] is not None # change inside api -> 'password hash'
        assert rv.json['updated fields']['email'] == TestAdmin.dummy_update_data['email']
        assert rv.json['updated fields']['is_admin'] == TestAdmin.dummy_update_data['is_admin']
        assert rv.json['updated fields']['max quota'] == TestAdmin.dummy_update_data['quota']

    def test_AdminUploadCSVResource(self, client):

        # first dataset is broken; contains a row with an existing id, nothing should be uploaded
        datasets = {'ActualTotalLoad': 0, 'AggregatedGenerationPerType': 3, 'DayAheadTotalLoadForecast': 3}

        for dataset, expected in datasets.items():
            # bad request without data
            rv = client.post('energy/api/Admin/' + dataset, headers=token_header(TestAdmin.admin_token))
            assert rv.status_code == 400

            with open(TestAdmin.source[dataset], 'rb') as f:
                # you shall not pass without admin token
                rv = client.post('energy/api/Admin/' + dataset, data=dict(file=(f, TestAdmin.source[dataset])), content_type='multipart/form-data')
                assert rv.status_code == 401

            with open(TestAdmin.source[dataset], 'rb') as f:
                # try to actually upload file
                rv = client.post('energy/api/Admin/' + dataset, headers=token_header(TestAdmin.admin_token), data=dict(file=(f, TestAdmin.source[dataset])), content_type='multipart/form-data')
                assert rv.status_code == 200

                # check stats of transaction
                print(rv.data)
                assert rv.json['totalRecordsImported']  == expected

    def test_BillingResource(self,client):
        # admin can't buy any billing plan
        rv = client.post('energy/api/Billing', data=TestAdmin.card_data, headers=token_header(TestAdmin.admin_token))
        assert rv.status_code == 400


    def test_LogoutResource(self, client):
        # fail without token
        rv = client.post('energy/api/Logout')
        assert rv.status_code == 401

        # fail with false token
        rv = client.post('energy/api/Logout', headers=token_header('false.token.hack'))
        #assert rv.status_code == 401

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
    endpoints = {'energy/api/ActualTotalLoad/Greece/PT60M/date/2018-01-09': (200,'json',user_quota),
                 'energy/api/ActualvsForecast/Elia%20CA/PT15M/date/2018-01-05?format=txt': (400,'txt',user_quota-1),                        # txt format unavailable
                 'energy/api/AggregatedGenerationPerType/Serbia/AllTypes/PT60M/month/2018-01?format=csv': (200,'csv',user_quota-1),
                 'energy/api/DayAheadTotalLoadForecast/Estonia/PT60M/year/2018?format=json': (200,'json',user_quota-2),
                 'energy/api/ActualvsForecast/Spain/PT60M/year/2018?format=csv': (200,'csv',user_quota-3),
                 'energy/api/AggregatedGenerationPerType/Greece/AncientGreekEnergy/PT60M/year/2018?format=csv': (400,'csv',user_quota-4),   # not yet :(
                 'energy/api/ActualvsForecast/Serbia/year/2016?format=csv': (404,'csv',user_quota-4),                                       # year 2016 doesn't exist
                 'energy/api/DayAheadTotalLoadForecast/North%20Macedonia/PT60M/year/2018': (403,'json',user_quota-4),                       # Not in Eu
                 'energy/api/DayAheadTotalLoadForecast/Italy/PT60M/month/2018-01': (402,'json',user_quota-5),                               # out of quota
                 'energy/api/ActualTotalLoad/Greece/PT60M/month/2018-01': (402,'json',user_quota-6)                                         # out of quota
                 }

    card_data = {
        'number' : "4444333322221111",
        'month' : 9,
        'year' : 2020,
        'cvc' : 135,
        'holder' : "Babababank",
        'plan' : "A"
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

    def test_UserResource(self, client):
        # you need a valid token for a registered user
        test_endpoint = list(TestUser.endpoints.keys())[0]
        rv = client.get(test_endpoint)
        assert rv.status_code == 401
        rv = client.get(test_endpoint, headers=token_header('false.token.hack'))
        assert rv.status_code == 422

        for endpoint,expected_response in TestUser.endpoints.items():
            rv = client.get(endpoint, headers=token_header(TestUser.user_token))
            print(endpoint)
            assert rv.status_code == expected_response[0]
            if rv.status_code == 200:
                assert rv.headers['Content-Type'].split("/")[1] == expected_response[1]
            elif rv.status_code == 402:
                assert expected_response[2] <= 0

    def test_BillingResource(self,client):
        # you can't buy any billing plan with a false or without token
        rv = client.post('energy/api/Billing', data=TestUser.card_data)
        assert rv.status_code == 401
        rv = client.post('energy/api/Billing', data=TestUser.card_data, headers=token_header('false.token.hack'))
        assert rv.status_code == 422

        # fail if something is missing
        rv = client.post('energy/api/Billing', data={k: v for k,v in TestUser.card_data.items() if k!= 'number'}, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400
        rv = client.post('energy/api/Billing', data={k: v for k,v in TestUser.card_data.items() if k!= 'month'}, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400
        rv = client.post('energy/api/Billing', data={k: v for k,v in TestUser.card_data.items() if k!= 'year'}, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400
        rv = client.post('energy/api/Billing', data={k: v for k,v in TestUser.card_data.items() if k!= 'cvc'}, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400
        rv = client.post('energy/api/Billing', data={k: v for k,v in TestUser.card_data.items() if k!= 'holder'}, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400
        rv = client.post('energy/api/Billing', data={k: v for k,v in TestUser.card_data.items() if k!= 'plan'}, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400

        # fail with expired card or wrong card details
        wrong_card = TestUser.card_data.copy()
        wrong_card['year'] = 2019
        rv = client.post('energy/api/Billing', data=wrong_card, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400
        wrong_card['year'] = 2020
        wrong_card['number'] = "4444333322226666"
        rv = client.post('energy/api/Billing', data=wrong_card, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400

        # you can buy one...
        rv = client.post('energy/api/Billing', data=TestUser.card_data, headers=token_header(TestUser.user_token))
        print(TestUser.card_data)
        assert rv.status_code == 200
        # ...but not two billing plans
        rv = client.post('energy/api/Billing', data=TestUser.card_data, headers=token_header(TestUser.user_token))
        assert rv.status_code == 400

    def test_LogoutResource(self, client):
        # fail without token
        rv = client.post('energy/api/Logout')
        assert rv.status_code == 401

        # fail with false token
        rv = client.post('energy/api/Logout', headers=token_header('false.token.hack'))
        assert rv.status_code == 422

        rv = client.post('energy/api/Logout', headers=token_header(TestUser.user_token))
        assert rv.status_code == 200
        TestUser.user_token = None
