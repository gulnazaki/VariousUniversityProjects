import pytest
from resources import app
from resources.models import db

# DO beforehand (*copy db to a test db*)
# 1. mysql > create database energy_db_test
# 2. mysqldump energy_db | mysql energy_db_test


@pytest.fixture(scope='session')
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/energy_db_test' # test database
    app.testing = True
    with app.app_context():
        # db.create_all()
        yield app.test_client()
        # db.session.remove()
        # db.drop_all()
