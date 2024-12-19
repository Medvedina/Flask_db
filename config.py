import os


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MegaSekretniyKey'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'MegaSekretniyKluch')


