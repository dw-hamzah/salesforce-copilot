from sqlalchemy import Column, DateTime, Integer, String, Numeric, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ProductInformation(Base):
    __tablename__ = 'product_information'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    product_description = Column(Text)
    uom = Column(String, nullable=False)

class TransactionData(Base):
    __tablename__ = 'transaction_data'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product_information.product_id'))
    qty = Column(Integer, nullable=False)
    price_snapshoot = Column(Numeric, nullable=False)
    total_price_snapshoot = Column(Numeric, nullable=False)
    sales_order_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey('customer_data.customer_id'))

class InventoryData(Base):
    __tablename__ = 'inventory_data'
    data_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product_information.product_id'))
    reorder_point = Column(Integer, nullable=False)

class PurchaseOrder(Base):
    __tablename__ = "purchase_order"
    purchase_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product_information.product_id'))
    received_qty = Column(Integer, nullable=False)

class CustomerData(Base):
    __tablename__ = 'customer_data'
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    customer_address = Column(String, nullable=False)
    customer_district = Column(String, nullable=False)
    customer_city = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 
