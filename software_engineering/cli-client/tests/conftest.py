import pytest
# from resources import app
# from resources.models import db, User
from click.testing import CliRunner

# DO beforehand (*copy db to a test db*)
# 1. mysql > create database energy_db_test
# 2. mysqldump energy_db | mysql energy_db_test

@pytest.fixture(scope='session')
def runner():
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/energy_db_test' # test database
    # app.testing = True
    # with app.app_context():
    #     db.session.begin_nested()
    #     yield CliRunner()
    #     db.session.rollback()
    return CliRunner()




