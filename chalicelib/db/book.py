import os
import sys
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import Session

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)
from chalicelib.db.connector import DECLARATIVE_BASE
from chalicelib.db.publisher import Publisher

sys.path.remove(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)


class Book(DECLARATIVE_BASE):

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey(Publisher.id), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    __tablename__ = "book"

    def __repr__(self):
        return f"Book id :{self.id} , title : {self.title} , price : {self.price}"

    @classmethod
    def get(
        cls,
        session: Session,
        id_list: List[int] = None,
        publisher_id_list: List[int] = None,
        price_lb: int = None,
        price_rb: int = None,
    ):

        query = session.query(cls)
        if id_list:
            query = query.filter(cls.id.in_(id_list))
        if publisher_id_list:
            query = query.filter(cls.publisher_id.in_(publisher_id_list))
        if price_lb is not None:
            query = query.filter(cls.price >= price_lb)
        if price_rb is not None:
            query = query.filter(cls.price <= price_rb)

        return query.all()
