from gluon.tools import Auth

# Make sure to match this with the models/db.py in welcome we we share auth tables
# settings.database_uri is set in 1.py, the local config file
db = DAL(settings.database_uri,pool_size=1,check_reserved=['all'])

auth = Auth(db)

# Note - welcome/models/db.py should have username=True to insure username field exists
auth.define_tables(username=True, migrate=False)

# Define our tables
db.define_table('lti_keys', Field('consumer'), Field('secret'), Field('application'))

# print "LTI db.py", type(db), type(auth)
