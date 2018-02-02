from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)

from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    bind=engine
))

Base = declarative_base()

Base.query = db_session.query_property()

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('employee',
                        uselist=True,
                        cascade='delete,all'))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
