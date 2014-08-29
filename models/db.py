from gluon.tools import Auth

# Make sure to match this with the models/db.py in welcome we we share auth tables
# settings.database_uri is set in 1.py, the local config file
db = DAL(settings.database_uri,pool_size=1,check_reserved=['all'])

auth = Auth(db)

##This is a kludge; need to copy the custom definition of auth_user from runestone/models/db.py, so that it will be able to insert user's course_id and section_id properly
##Also had to include a copy of db_sections.py from the runestone app; have to keep that in sync with what's there.
db.define_table('auth_user',
    Field('username', type='string',
          label=T('Username')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('email', type='string',
          requires=IS_EMAIL(banned='^.*shoeonlineblog\.com$'),
          label=T('Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('registration_key',default='',
          writable=False,readable=False),
    Field('reset_password_key',default='',
          writable=False,readable=False),
    Field('registration_id',default='',
          writable=False,readable=False),
    Field('cohort_id','reference cohort_master', requires=IS_IN_DB(db, 'cohort_master.id', 'id'),
          writable=False,readable=False),
    Field('course_id',db.courses,label=T('Course Name'),
          required=True,
          default=1),
    Field('course_name',compute=lambda row: getCourseNameFromId(row.course_id)),
#    format='%(username)s',
    format=lambda u: u.first_name + " " + u.last_name,
    migrate='runestone_auth_user.table')


db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
db.auth_user.course_id.requires = IS_COURSE_ID()
# Note - welcome/models/db.py should have username=True to insure username field exists
auth.define_tables(username=True, migrate=False)

# Define our tables
db.define_table('lti_keys', Field('consumer'), Field('secret'), Field('application'))

# print "LTI db.py", type(db), type(auth)
