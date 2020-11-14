import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    mysql_db_username = 'leandropaixao'
    mysql_db_password = 'Mys$Desenv81'
    mysql_db_name = 'calendrier'
    mysql_db_hostname = 'localhost:3306'

    SECRET_KEY = os.environ.get('SECRET_KET') or 'vous-ne-pouvez-pas-passer'
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(mysql_db_username,
        mysql_db_password, mysql_db_hostname,mysql_db_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
