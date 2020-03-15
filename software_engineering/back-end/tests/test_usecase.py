import pytest
from resources.config import FREE_QUOTA_PER_MINUTE
from resources.models import User
from .utils import token_header

class TestUseCase1(object):
    admin_data = {
        'username': 'admin',
        'password': '321nimda'
    }
    admin_token = None
    user_data = {
        'username': 'molly',
        'password': '12345',
        'email':    'candy@myworld.fr',
        'quota': 1
    }
    user_token = None
    card_data = {
        'number' : "4444333322221111",
        'month' : 9,
        'year' : 2020,
        'cvc' : 135,
        'holder' : "Babababank",
        'plan' : "A"
    }


    def test_scenario(self, client):

        # molly tries to login, but fails
        rv = client.post('energy/api/Login', data={k: TestUseCase1.user_data[k] for k in ['username', 'password']})
        assert rv.status_code == 401                                                                                # <-- it should yield 401, not 400

        # molly calls admin. admin just woke up, forgot to add molly's account yesterday
        # he tries to login
        rv = client.post('energy/api/Login', data=TestUseCase1.admin_data)
        assert rv.status_code == 200
        assert rv.json['token'] is not None
        TestUseCase1.admin_token = rv.json['token']

        # then he adds her
        rv = client.post('energy/api/Admin/users', headers=token_header(TestUseCase1.admin_token), data=TestUseCase1.user_data)
        assert rv.status_code == 200

        # he texts her: 'I got you'
        # she sceptically tries to login
        rv = client.post('energy/api/Login', data={k: TestUseCase1.user_data[k] for k in ['username', 'password']})
        assert rv.status_code == 200
        assert rv.json['token'] is not None
        TestUseCase1.user_token = rv.json['token']

        # suprsingly, the admin was right and she, happily, tries to check how's been doing her favorite energy factory in greece
        rv = client.get('energy/api/ActualTotalLoad/Greece/PT60M/date/2018-01-09', headers=token_header(TestUseCase1.user_token))
        assert rv.status_code == 200

        # all look good. The data seem right. What about her beloved Spain?
        rv = client.get('energy/api/ActualvsForecast/Spain/PT60M/year/2018?format=csv', headers=token_header(TestUseCase1.user_token))
        assert rv.status_code == 402

        # she furiously calls admin:
        # - 'wtf dude? What is this "402 Payment Required" bullshit?'
        # - 'hold on, baby. let me check'
        rv = client.get('energy/api/Admin/users/' + TestUseCase1.user_data['username'], headers=token_header(TestUseCase1.admin_token))
        assert rv.status_code == 200
        assert rv.json['current quota'] == 0

        # - 'yeah, you still on the line? You need to pay to see more, I'm sorry.
        # - '@%#^%$%&'
        rv = client.post('energy/api/Billing', data=TestUseCase1.card_data, headers=token_header(TestUseCase1.user_token))
        assert rv.status_code == 200

        # she may have spend all of hers cat food money on a questionable observatory with an alcooholic, sexist admin, but at least
        # she hopes she can now view spain's Actual vs Forecast!!
        rv = client.get('energy/api/ActualvsForecast/Spain/PT60M/year/2018?format=csv', headers=token_header(TestUseCase1.user_token))
        assert rv.status_code == 200

        # "pheww"
