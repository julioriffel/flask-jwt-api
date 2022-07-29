from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import Text

from app.app import db


class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False, default=0)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, name, price, description, quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, name=None, price=None, description=None, quantity=None):
        if name:
            self.name = name
        if price:
            self.price = price
        if description:
            self.description = description
        if quantity:
            self.quantity = quantity
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
