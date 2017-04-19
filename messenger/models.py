# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_FULL_ENGINE

engine = create_engine(DB_FULL_ENGINE)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    password = Column(String(20))
    ip_list = Column(String(200), nullable=True) # kokos

    def __init__(self, name, password, ip_list):
        self.name = name
        self.password = password
        self.ip_list = ip_list

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.password, self.ip_list)

