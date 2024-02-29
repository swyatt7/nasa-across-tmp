import os

class Config(object):
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    DB_USER = os.environ.get('DB_USER', 'across_admin')
    DB_PWD = os.environ.get('DB_PWD', '') #Ar0undTheW0rld
    DB_NAME = os.environ.get('DB_NAME', 'acrossdev')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'postgresql://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
config = Config()