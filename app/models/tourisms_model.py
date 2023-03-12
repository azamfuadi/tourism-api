from sqlalchemy.orm import relationship
from app import mysql_engine, Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, TIMESTAMP, Table, DateTime


class UserPlans(Base):
    __tablename__ = 'user_plans'

    plan_id = Column(String(32), ForeignKey('plans.id'),
                     primary_key=True, nullable=False)
    user_id = Column(String(32), ForeignKey('users.id'),
                     primary_key=True, nullable=False)
    user_role = Column(String(50), nullable=True)

    users = relationship('Users', back_populates="plans")
    plans = relationship('Plans', back_populates="users")


class TourismPlans(Base):
    __tablename__ = 'tourism_plans'

    plan_id = Column(String(32), ForeignKey('plans.id'),
                     primary_key=True, nullable=False)
    tourism_id = Column(String(32), ForeignKey('tourisms.id'),
                        primary_key=True, nullable=False)
    date = Column(DateTime, nullable=True)

    tourisms = relationship('Tourisms', back_populates="plans")
    plans = relationship('Plans', back_populates="tourisms")


class Tourisms(Base):
    __tablename__ = 'tourisms'
    id = Column(String(32), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    img_url = Column(String(255), nullable=True)
    contact = Column(String(50), nullable=True)
    schedule = Column(String(200), nullable=True)

    plans = relationship("TourismPlans", back_populates="tourisms")


class Plans(Base):
    __tablename__ = 'plans'
    id = Column(String(32), primary_key=True, nullable=False)
    destination = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    note = Column(String(255), nullable=True)
    start_date = Column(DateTime, nullable=True)
    finish_date = Column(DateTime, nullable=True)

    tourisms = relationship("TourismPlans", back_populates="plans")
    users = relationship("UserPlans", back_populates="plans")


Base.metadata.create_all(mysql_engine, checkfirst=True)
