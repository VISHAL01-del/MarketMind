from sqlalchemy import Column,Integer,Float
from src.database.connection import Base

class CustomerDB(Base):
    __tablename__="customers"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    membership_years = Column(Integer, nullable=False)
    total_orders = Column(Integer, nullable=False)
    average_order_value = Column(Float, nullable=False)
    days_since_last_purchase = Column(Integer, nullable=False)
    total_spending = Column(Float, nullable=False)