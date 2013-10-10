# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)







db.define_table('courses',							#The courses the institution offers
	  Field('name','string'),
	  Field('credits','integer',requires=IS_IN_SET([1,2,3,4,5])))

db.define_table('faculty',
	  Field('name',requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name')),
	  Field('courses',requires=IS_IN_SET(['Data Structures','ITWS II','Maths-II','Basic Electronic Circuits','Computer Systems Organisations'])),
	  Field('designation',requires=IS_IN_SET(['Professor','Assistant_Professor','Lecturer'])))

db.define_table('student',
	  Field('email',readable=False,writable=False),
	  Field('institution_name','string',notnull=True),
	  Field('courses_taken',requires=IS_IN_DB(db,'courses.id','courses.name')),
	  Field('date_of_birth','date',notnull=True),
	  Field('fathers_name','string',notnull=True),
	  Field('mothers_name','string',notnull=True),
	  Field('address','text',notnull=True),
	  Field('coun','integer',readable=False,writable=False),
	  Field('final_marks','integer',readable=False,writable=False),
	  Field('your_photo','upload',notnull=True)
	  )

db.define_table('questions',
	  Field('faculty_id','string',readable=False,writable=False),
	  Field('course',requires=IS_IN_DB(db,'courses.id','courses.name')),
	  Field('que_number','integer'),
	  Field('question','string'),
	  Field('option_a','string'),
	  Field('option_b','string'),
	  Field('option_c','string'),
	  Field('option_d','string'),
	  Field('ans',requires=IS_IN_SET(['A','B','C','D'],multiple=True),widget=SQLFORM.widgets.checkboxes.widget),
	  Field('maxmarks','integer'),
	  Field('stid','string',readable=False,writable=False),
	  Field('obtained_marks','integer',default=0,readable=False,writable=False)
	  )
db.define_table('answer',
	  Field('course','integer',readable=False,writable=False),
	  Field('stid','string',readable=False,writable=False),
	  Field('que_num','integer',readable=False,writable=False),
	  Field('op',requires=IS_IN_SET(['A','B','C','D'],multiple=True),widget=SQLFORM.widgets.checkboxes.widget),
	  Field('given','integer',default=0,readable=False,writable=False)
	  )

db.define_table('see',
	  Field('course','integer'))

db.define_table('comments',
	  Field('que','integer'),
	  Field('faculty_id','string'),
	  Field('course','string'),
	  Field('comment_given','text'))

db.define_table('times',
	  Field('course',requires=IS_IN_DB(db,'courses.id','courses.name')),
	  Field('date_of_exam','string'),
	  Field('start_time','time'),
	  Field('end_time','time'))
