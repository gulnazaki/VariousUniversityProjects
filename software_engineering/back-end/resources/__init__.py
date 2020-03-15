from flask_restful import Api
from flask import Flask
from flask_jwt_extended import JWTManager, get_jwt_identity
from werkzeug.exceptions import BadRequest, Unauthorized, ServiceUnavailable
from resources.models import db, bcrypt, User, LoggedOutTokens
from resources.utils import (
    DatasetConverter,
    ResolutionConverter,
    DateConverter,
    MonthConverter,
    YearConverter
)
import resources.utils as utils
from resources.config import Config

# resources/endpoints
from resources.access import (
    LoginResource,
    LogoutResource,
    AccountResource
)

from resources.admin import (
    AdminUserResource,
    AdminGetOrEditUserResource,
    AdminUploadCSVResource
)

from resources.subsidiary import (
    HealthCheckResource,
    ResetResource,
    HardResetResource,
    ContactResource
)

from resources.billing import (
    BillingResource,
    BillingPlansResource
)

### Step 1: create the app
app = Flask(__name__)

app.config.from_object(Config)
app.url_map.converters['dataset'] = DatasetConverter
app.url_map.converters['resolution'] = ResolutionConverter
app.url_map.converters['date'] = DateConverter
app.url_map.converters['month'] = MonthConverter
app.url_map.converters['year'] = YearConverter

### Step 2: Create the Rest API
api = Api(prefix='/energy/api')

### Step 3: Bind resources (i.e. endpoints) to the API
from resources.dataviews import ATL, AGPT, DATLF, ATLvsDATLF

# user access resources/endpoints
api.add_resource(LoginResource, '/Login')
api.add_resource(LogoutResource, '/Logout')
api.add_resource(AccountResource, '/Account')

# administrative resources/endpoints
api.add_resource(AdminUserResource, '/Admin/users')
api.add_resource(AdminGetOrEditUserResource, '/Admin/users/<string:username>')
api.add_resource(AdminUploadCSVResource, '/Admin/<dataset:dataset>')

# subsidiary resources/endpoints
api.add_resource(HealthCheckResource, '/HealthCheck')
api.add_resource(ResetResource, '/Reset')
api.add_resource(HardResetResource, '/Reset/HARD')
api.add_resource(ContactResource, '/Contact')

# billing endpoints
api.add_resource(BillingResource, '/Billing')
api.add_resource(BillingPlansResource, '/BillingPlans')

# data resources/endpoints
ATL_base_url = '/ActualTotalLoad/<string:areaname>/<resolution:resolution>/'
AGPT_base_url = '/AggregatedGenerationPerType/<string:areaname>/<path:prod_type>/<resolution:resolution>/'
DATLF_base_url = '/DayAheadTotalLoadForecast/<string:areaname>/<resolution:resolution>/'
ATLvsDATLF_base_url = '/ActualvsForecast/<string:areaname>/<resolution:resolution>/'

d_url = 'date/<date:date>'
m_url = 'month/<month:month>'
y_url = 'year/<year:year>'

api.add_resource(ATL, ATL_base_url + d_url, ATL_base_url + m_url, ATL_base_url + y_url)
api.add_resource(AGPT, AGPT_base_url + d_url, AGPT_base_url + m_url, AGPT_base_url + y_url)
api.add_resource(DATLF, DATLF_base_url + d_url, DATLF_base_url + m_url, DATLF_base_url + y_url)
api.add_resource(ATLvsDATLF, ATLvsDATLF_base_url + d_url, ATLvsDATLF_base_url + m_url, ATLvsDATLF_base_url + y_url)

### Step 4: bind the app with the API, the database, the crypto-module and the JWT manager
api.init_app(app)
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

### Step 5: configure the JWT manager

# to distinguish simple user from admin
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return { 'is_admin': user.is_admin }

# to get the identity of the user from the JWT
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

# to return the user (from the database) that corresponds to this identity
@jwt.user_loader_callback_loader
def user_loader(username):
    try:
        user = User.query.filter_by(username=username).first()
    except:
        raise ServiceUnavailable('Database error')
    return user

# is called when the above function returns None
@jwt.user_loader_error_loader
def on_failed_user_lookup(username):
    raise Unauthorized(f"the API key provided was issued for the user '{username}' that no longer exists")

# store the revoked JWTs (after logout) until they expire
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    try:
        ret = LoggedOutTokens.query.filter_by(jti=jti).first()
    except:
        raise ServiceUnavailable('Database error')
    return ret is not None
