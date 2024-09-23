from sqlalchemy.ext.declarative import declarative_base

# all the models should register here!
from .auth_models import User

Base = declarative_base()