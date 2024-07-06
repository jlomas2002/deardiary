import os
from dotenv import load_dotenv

load_dotenv(os.path.join(basedir, '.env'))

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True 

WTF_CSRF_ENABLED = True
SECRET_KEY = os.getenv('SECRET_KEY')