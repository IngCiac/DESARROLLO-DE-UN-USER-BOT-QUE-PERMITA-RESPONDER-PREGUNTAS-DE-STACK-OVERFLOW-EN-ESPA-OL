import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connection: str = 'mssql+pyodbc://{username}:{password}@{hostname}:{port}/{database}?driver={driver}'.format(
    username = 'sa',#os.getenv('DATABASE_USERNAME'),
    password = '0953705787',#os.getenv('DATABASE_PASSWORD'),
    hostname = '127.0.0.1',#os.getenv('DATABASE_HOSTNAME'),
    port = '1433',#os.getenv('DATABASE_PORT'),
    database = 'chatbot',#os.getenv('DATABASE_NAME'),
    driver = 'ODBC Driver 17 for SQL Server'
)

engine = sqlalchemy.create_engine(connection)
#engine = sqlalchemy.create_engine('sqlite:///database/database.sqlite3')

Session = sessionmaker(
    bind = engine
)
Base = declarative_base()
session = Session()
