
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'top secret'
    JWT_ACCESS_LIFESPAN = {'hours': 24}
    JWT_REFRESH_LIFESPAN = {'days': 30}
