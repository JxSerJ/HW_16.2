from sqlalchemy.orm import sessionmaker

from config import DATABASE_PATH
from sqlalchemy import create_engine

# An Engine, which the Session will use for connection to the database.
engine = create_engine(f'sqlite:///{DATABASE_PATH}')

Session = sessionmaker(bind=engine)
