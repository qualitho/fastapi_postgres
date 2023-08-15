from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# setup for the database connection 
# path with username and pw
URL_DATABASE = 'postgresql://postgres:1307@localhost:5432/QuizApp'

# database engine
engine = create_engine(URL_DATABASE)

# local session
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()