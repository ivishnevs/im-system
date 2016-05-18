import sqlalchemy
from config import DB_ENGINE, DB_NAME, DB_HOST, DB_PASSWORD, DB_USER, DB_FULL_ENGINE


with sqlalchemy.create_engine(
    DB_ENGINE + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/',
    isolation_level='AUTOCOMMIT'
).connect() as conn:
    conn.execute('CREATE DATABASE '+DB_NAME+';')

engine = sqlalchemy.create_engine(DB_FULL_ENGINE)

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(20), unique=True),
    Column('password', String(20)),
    Column('ip_list', String(200), nullable=True),
)
metadata.create_all(engine)
