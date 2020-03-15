from cli import cli
import os
import random, string

class TestAdmin(object):

    admin_data = {
        'username': 'admin',
        'passw':    '321nimda'
    }

    def test_login(self, runner):
        # login admin with correct credentials
        result = runner.invoke(cli, ['Login', '--username', TestAdmin.admin_data['username'], '--passw', TestAdmin.admin_data['passw']])
        assert result.exit_code == 0

        # logout
        runner.invoke(cli, ['Logout'])

        # wrong username
        result = runner.invoke(cli, ['Login', '--username', 'oops', '--passw', TestAdmin.admin_data['passw']])
        assert result.exit_code == 42

        # wrong password
        result = runner.invoke(cli, ['Login', '--username', TestAdmin.admin_data['username'], '--passw', 'oops'])
        assert result.exit_code == 42

        # Login when loggedin
        runner.invoke(cli, ['Login', '--username', TestAdmin.admin_data['username'], '--passw', TestAdmin.admin_data['passw']])
        result = runner.invoke(cli, ['Login', '--username', TestAdmin.admin_data['username'], '--passw', TestAdmin.admin_data['passw']])
        assert result.exit_code == 1

        # logout
        runner.invoke(cli, ['Logout'])

        # Logout when loggedout
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 1

    def test_MutuallyExclusive(self, runner):

        # For the following must be logged in as admin
        runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])

        # newuser is M_E with userstatus
        result = runner.invoke(cli, ['Admin', '--newuser', 'kostas', '--passw', 'mlpamlpa', '--email', 'mlpamlpa@gmail.com', '--userstatus', 'kostas'])
        assert result.exit_code == 2

        # newuser is M_E with moduser
        result = runner.invoke(cli, ['Admin', '--newuser', 'kostas', '--passw', 'mlpamlpa', '--email', 'mlpamlpa@gmail.com', '--moduser', 'kostas', '--passw', 'mlpamlpa', '--email', 'mlpamlpa@gmail.com'])
        assert result.exit_code == 2

        # newuser is M_E with newdata
        result = runner.invoke(cli, ['Admin', '--newuser', 'kostas', '--passw', 'mlpamlpa', '--email', 'mlpamlpa@gmail.com', '--newdata', 'ActualTotalLoad', '--source', 'csv'])
        assert result.exit_code == 2

        # newuser is M_E with deluser
        result = runner.invoke(cli, ['Admin', '--newuser', 'kostas', '--passw', 'mlpamlpa', '--email', 'mlpamlpa@gmail.com', '--deluser', 'kostas'])
        assert result.exit_code == 2

    def test_AdminRequirments(self, runner):

        # moduser --> must provide username
        result = runner.invoke(cli, ['Admin', '--moduser'])
        assert result.exit_code == 2

        # newuser --> must provide username
        result = runner.invoke(cli, ['Admin', '--newuser'])
        assert result.exit_code == 2

        # newdata --> must provide the table
        result = runner.invoke(cli, ['Admin', '--newdata'])
        assert result.exit_code == 2

        # userstatus --> must provide username
        result = runner.invoke(cli, ['Admin', '--userstatus'])
        assert result.exit_code == 2

        # deluser --> must provide username
        result = runner.invoke(cli, ['Admin', '--deluser'])
        assert result.exit_code == 2

        # newuser --> passw and email are required
        result = runner.invoke(cli, ['Admin', '--newuser', 'kostas', '--passw', 'mlpamlpa'])
        assert result.exit_code == 1

        # moduser --> passw or email or quota is required
        result = runner.invoke(cli, ['Admin', '--moduser', 'kostas'])
        assert result.exit_code == 1

        # newdata --> must provide CSV file
        result = runner.invoke(cli, ['Admin', '--newdata', 'ActualTotalLoad'])
        assert result.exit_code == 1

    def test_deluser(self,runner):

        def randomword(length):
           letters = string.ascii_lowercase
           return ''.join(random.choice(letters) for i in range(length))

        rdom_user_data = {
        'username' : randomword(10),
        'passw' : randomword(10),
        'email' : randomword(10)
        }

        #create a new user
        result = runner.invoke(cli, ['Admin', '--newuser', rdom_user_data['username'], '--passw', rdom_user_data['passw'], '--email', rdom_user_data['email']])
        assert result.exit_code == 0

        #delete the user
        result = runner.invoke(cli, ['Admin', '--deluser', rdom_user_data['username']], input='y\n')
        assert result.exit_code == 0

        #delete this user again
        result = runner.invoke(cli, ['Admin', '--deluser', rdom_user_data['username']], input='y\n')
        print(result.output)
        assert result.exit_code == 42

    def test_SourcePath(self, runner):

        # source must be a path
        result = runner.invoke(cli, ['Admin', '--newdata', 'ActualTotalLoad', '--source', 'NotaValidPath'])
        assert result.exit_code == 2

        # Admin logout 
        runner.invoke(cli, ['Logout'])

class TestActualTotalLoad(object):

    def test_AreYouLoggedin(self,runner):

        # Not loggedin
        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018' ])
        assert result.exit_code == 1

        #Login
        result = runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])
        assert result.exit_code == 0

        #Try again
        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018' ])
        print(result.output)
        assert result.exit_code == 0

        #Logout
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 0

    def test_MutuallyExclusive(self, runner):

        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--month', '2018-1', '--date', '2018-1-1' ])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--month', '2018-1'])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--date', '2018-1-1' ])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--month', '2018-1', '--date', '2018-1-1' ])
        assert result.exit_code == 2

    def test_Required(self, runner):

        # area is required
        result = runner.invoke(cli, ['ActualTotalLoad', '--timeres', 'PT60M', '--year', '2018'])
        assert result.exit_code == 2

        # timeres is required
        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--year', '2018'])
        assert result.exit_code == 2

        #date or motnh or year is required
        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M'])
        assert result.exit_code == 1

class TestAggregatedGenerationPerType(object):

    def test_AreYouLoggedin(self,runner):

        # Not loggedin
        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--area', 'Greece', '--timeres', 'PT60M', '--prodactiontype', 'Alltypes', '--year', '2018' ])
        assert result.exit_code == 2

        #Login
        result = runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])
        assert result.exit_code == 0

        #Try again
        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018' ])
        assert result.exit_code == 0

        #Logout
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 0

    def test_MutuallyExclusive(self, runner):

        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--area', 'Greece', '--timeres', 'PT60M', '--prodactiontype', 'Alltypes', '--year', '2018', '--month', '2018-1', '--date', '2018-1-1' ])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--area', 'Greece', '--timeres', 'PT60M',  '--prodactiontype', 'Alltypes', '--year', '2018', '--month', '2018-1'])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--area', 'Greece', '--timeres', 'PT60M',  '--prodactiontype', 'Alltypes', '--year', '2018', '--date', '2018-1-1' ])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--area', 'Greece', '--timeres', 'PT60M', '--prodactiontype', 'Alltypes', '--month', '2018-1', '--date', '2018-1-1' ])
        assert result.exit_code == 2

    def test_Required(self, runner):

        # area is required
        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--timeres', 'PT60M', '--prodactiontype', 'Alltypes','--year', '2018'])
        assert result.exit_code == 2

        # timeres is required
        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--area', '--prodactiontype', 'Alltypes', 'Greece', '--year', '2018'])
        assert result.exit_code == 2

        # productiontype is required
        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--area', 'Greece', 'timeres', 'PT60M' , '--year', '2018'])
        assert result.exit_code == 2

        #date or month or year is required
        result = runner.invoke(cli, ['AggregatedGenerationPerType', '--area', 'Greece', '--timeres', 'PT60M', '--prodactiontype', 'Alltypes'])
        assert result.exit_code == 2

class TestDayAheadTotalLoadForecast(object):

    def test_AreYouLoggedin(self,runner):

        # Not loggedin
        result = runner.invoke(cli, ['DayAheadTotalLoadForecast', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018' ])
        assert result.exit_code == 1

        #Login
        result = runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])
        assert result.exit_code == 0

        #Try again
        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018' ])
        assert result.exit_code == 0

        #Logout
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 0

    def test_MutuallyExclusive(self, runner):

        result = runner.invoke(cli, ['DayAheadTotalLoadForecast', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--month', '2018-1', '--date', '2018-1-1' ])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['DayAheadTotalLoadForecast', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--month', '2018-1'])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['DayAheadTotalLoadForecast', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--date', '2018-1-1' ])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['DayAheadTotalLoadForecast', '--area', 'Greece', '--timeres', 'PT60M', '--month', '2018-1', '--date', '2018-1-1' ])
        assert result.exit_code == 2

    def test_Required(self, runner):

        # area is required
        result = runner.invoke(cli, ['DayAheadTotalLoadForecast', '--timeres', 'PT60M', '--year', '2018'])
        assert result.exit_code == 2

        # timeres is required
        result = runner.invoke(cli, ['DayAheadTotalLoadForecast', '--area', 'Greece', '--year', '2018'])
        assert result.exit_code == 2

        #date or motnh or year is required
        result = runner.invoke(cli, ['DayAheadTotalLoadForecast', '--area', 'Greece', '--timeres', 'PT60M'])
        assert result.exit_code == 1

class TestActualvsForecast(object):

    def test_AreYouLoggedin(self,runner):

        # Not loggedin
        result = runner.invoke(cli, ['ActualvsForecast', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018' ])
        assert result.exit_code == 1

        #Login
        result = runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])
        assert result.exit_code == 0

        #Try again
        result = runner.invoke(cli, ['ActualTotalLoad', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018' ])
        assert result.exit_code == 0

        #Logout
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 0

    def test_MutuallyExclusive(self, runner):

        result = runner.invoke(cli, ['ActualvsForecast', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--month', '2018-1', '--date', '2018-1-1' ])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['ActualvsForecast', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--month', '2018-1'])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['ActualvsForecast', '--area', 'Greece', '--timeres', 'PT60M', '--year', '2018', '--date', '2018-1-1' ])
        assert result.exit_code == 2

        result = runner.invoke(cli, ['ActualvsForecast', '--area', 'Greece', '--timeres', 'PT60M', '--month', '2018-1', '--date', '2018-1-1' ])
        assert result.exit_code == 2

    def test_Required(self, runner):

        # area is required
        result = runner.invoke(cli, ['ActualvsForecast', '--timeres', 'PT60M', '--year', '2018'])
        assert result.exit_code == 2

        # timeres is required
        result = runner.invoke(cli, ['ActualvsForecast', '--area', 'Greece', '--year', '2018'])
        assert result.exit_code == 2

        #date or month or year is required
        result = runner.invoke(cli, ['ActualvsForecast', '--area', 'Greece', '--timeres', 'PT60M'])
        assert result.exit_code == 1

class TestUserLoggin(object):

    def test_login(self, runner):

        def randomword(length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))

        rdom_user_data = {
            'username' : randomword(10),
            'passw' : randomword(10),
            'email' : randomword(10)
        }

        #create a new user to test user login-logout
        runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])
        runner.invoke(cli, ['Admin', '--newuser', rdom_user_data['username'], '--passw', rdom_user_data['passw'], '--email', rdom_user_data['email']])
        runner.invoke(cli, ['Logout'])

        # login user with correct credentials
        result = runner.invoke(cli, ['Login', '--username', rdom_user_data['username'], '--passw', rdom_user_data['passw']])
        assert result.exit_code == 0

        # logout
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 0

        # wrong username
        result = runner.invoke(cli, ['Login', '--username', 'oops', '--passw', rdom_user_data['passw']])
        assert result.exit_code == 42

        # wrong password
        result = runner.invoke(cli, ['Login', '--username', rdom_user_data['username'], '--passw', 'oops'])
        assert result.exit_code == 42

        # Login when loggedin
        result = runner.invoke(cli, ['Login', '--username', rdom_user_data['username'], '--passw', rdom_user_data['passw']])
        assert result.exit_code == 0

        result = runner.invoke(cli, ['Login', '--username', rdom_user_data['username'], '--passw', rdom_user_data['passw']])
        assert result.exit_code == 1

        # logout
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 0

        # Logout when loggedout
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 1

        #delete the user
        result = runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])
        assert result.exit_code == 0
        assert 'Login successful. Welcome to electra, admin' in result.output

        runner.invoke(cli, ['Admin', '--deluser', rdom_user_data['username']], input='y\n')
        assert result.exit_code == 0

        runner.invoke(cli, ['Logout'])
        assert result.exit_code == 0
