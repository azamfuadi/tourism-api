from sqlalchemy.orm import relationship
from app import mysql_engine, Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, TIMESTAMP, Table, DateTime


class UserPlans(Base):
    __tablename__ = 'user_plans'
    id = Column(String(32), primary_key=True, nullable=False),
    user_role = Column(String(50), nullable=False),
    plan_id = Column(String(32), ForeignKey('plans.id'), primary_key=True)
    user_id = Column(String(32), ForeignKey('users.id'), primary_key=True)

    users = relationship('Users', back_populates="plans")
    plans = relationship('Plans', back_populates="users")


class Tourisms(Base):
    __tablename__ = 'tourisms'
    id = Column(String(32), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    img_url = Column(String(255), nullable=True)

    plan = relationship("Plans", back_populates="tourisms")


class Plans(Base):
    __tablename__ = 'plans'
    id = Column(String(32), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    note = Column(String(255), nullable=True)
    itinerary = Column(String(255), nullable=True)
    start_date = Column(DateTime, nullable=True)
    finish_date = Column(DateTime, nullable=True)

    tourism_id = Column(String(32), ForeignKey('tourisms.id'), nullable=False)

    tourisms = relationship("Tourisms", back_populates="plan", uselist=False)
    users = relationship("UserPlans", back_populates="plans")


Base.metadata.create_all(mysql_engine, checkfirst=True)
