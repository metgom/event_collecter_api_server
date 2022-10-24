from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.config import server_config


_db_id = server_config["AWS_RDS"]["AWS_RDS_ID"]
_db_pw = server_config["AWS_RDS"]["AWS_RDS_PW"]
_db_host = server_config["AWS_RDS"]["AWS_RDS_URL"]
_db_port = server_config["AWS_RDS"]["AWS_RDS_PORT"]
_db_name = server_config["AWS_RDS"]["AWS_RDS_DBNAME"]
_db_conn = f'mysql+pymysql://{_db_id}:{_db_pw}@{_db_host}:{_db_port}/{_db_name}'

engine = create_engine(_db_conn)
ORMSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ORMBase = declarative_base()


def close_db():
    global engine
    if engine is not None:
        engine.dispose()


def get_db_session():
    return ORMSession()
