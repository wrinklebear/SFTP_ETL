#! /usr/bin/python
# coding=utf-8

import pymssql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Float, Integer, String
from settings import *


Base = declarative_base()
engine = create_engine(DB_CONNECT_STRING, echo=True)
Base.metadata.reflect(engine)
tables = Base.metadata.tables
# print(tables)
# for t, v in enumerate(set(tables.items())):
#     print(v)
#     for i in v:
#         print(i)
#         print("\n")


class ShopperProfile(Base):
    __tablename__ = 'ShopperProfile'
    __table_args__ = {"useexisting": True}

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    crowdName = Column(String(50))
    itemName = Column(String(50))
    TGI = Column(Float)
    Percentage = Column(Float)
    Dim = Column(String(50))
    fileName = Column(String(50))
    uploadTime = Column(String(50))
    createTime = Column(String(50))

    def __init__(self, username, email):
        self.fileName = fileName
        self.Dim = Dim

    def __repr__(self):
        return '<ShopperProfile %r>' % self.fileName

# 根据模型建表
Base.metadata.create_all(engine)
