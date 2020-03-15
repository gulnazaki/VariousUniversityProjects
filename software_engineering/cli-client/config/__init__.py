import os

# adding the 2 lines below to supress the warning that our self-signed ertificate has no `subjectAltName`
import urllib3
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

ELECTRA_API_ADDRESS = 'https://localhost:8765/energy/api'
USER_HOME = os.path.expanduser('~')
APIKEY_FILE = USER_HOME + '/softeng19bAPI.token'
APIKEY_HEADER_NAME = 'x-observatory-auth'
API_CERT_LOC = os.path.join(os.pardir, 'back-end', '.certs', 'cert.pem')
