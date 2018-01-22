import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES = {}
DATABASES['default'].update(db_from_env)

# import os
#
# DB_NAME = os.environ["DB_NAME"]
# DB_USER = os.environ["DB_USER"]
# DB_PWD = os.environ["DB_PWD"]
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': DB_NAME,
#         'USER' : DB_USER,
#         'PASSWORD' : DB_PWD,
#         'HOST' : '127.0.0.1',
#         'PORT' : '5432',
#     }
# }