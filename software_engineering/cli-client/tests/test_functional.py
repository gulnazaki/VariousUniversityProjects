from cli import cli
import os

class TestIfApiKeySaved(object):

    def test_ifSavedForUser(self, runner):

        #create a user to check
        runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])
        runner.invoke(cli, ['Admin', '--newuser', 'allosxr', '--passw', 'rxsolla', '--email', 'amanaman@hotmail.com'])
        runner.invoke(cli, ['Logout'])
        runner.invoke(cli, ['Login', '--username', 'allosxr', '--passw', 'rxsolla'])

        USER_HOME = os.path.expanduser('~')
        file_path = USER_HOME + '/softeng19bAPI.token'

        # I am logged in I must have apikey
        assert os.path.exists(file_path)
        assert os.stat(file_path).st_size != 0

        runner.invoke(cli, ['Logout'])
        # I am logged out I dont have apikey
        assert os.path.exists(file_path) == False

        #delete the user
        result = runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])
        assert result.exit_code == 0
        result = runner.invoke(cli, ['Admin', '--deluser', 'allosxr'], input='y\n')
        assert result.exit_code == 0
        result = runner.invoke(cli, ['Logout'])
        assert result.exit_code == 0

    def test_ifSavedForAdmin(self, runner):

        runner.invoke(cli, ['Login', '--username', 'admin', '--passw', '321nimda'])

        USER_HOME = os.path.expanduser('~')
        file_path = USER_HOME + '/softeng19bAPI.token'

        # I am logged in I must have apikey
        assert os.path.exists(file_path)
        assert os.stat(file_path).st_size != 0

        runner.invoke(cli, ['Logout'])
        # I am logged out I dont have apikey
        assert os.path.exists(file_path) == False
