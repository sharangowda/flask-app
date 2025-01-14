import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI', 'sqlite:///posts_data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-key')
    DEBUG = False
