from sqlalchemy.orm import relationship
from app import mysql_engine, Base
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, true, TIMESTAMP


class Users(Base):
    __tablename__ = 'users'
    id = Column(String(32), primary_key=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    username = Column(String(100), nullable=True)
    prof_pic = Column(String(255), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    gender = Column(String(50), nullable=True)

    plans = relationship("UserPlans", back_populates="users")


Base.metadata.create_all(mysql_engine, checkfirst=True)
