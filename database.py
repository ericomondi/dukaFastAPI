from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

password = 'dmore#2020'
URL_DATABASE = f'mysql+pymysql://root:{password}@localhost:3306/dukaapp'
engine =create_engine(URL_DATABASE)

# URL_DATABASE = 'sqlite:///./todosapp.db'
# engine = create_engine(URL_DATABASE, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()