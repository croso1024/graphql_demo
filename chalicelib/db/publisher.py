import os
import sys
from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)
from chalicelib.db.connector import DECLARATIVE_BASE

sys.path.remove(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)


class Publisher(DECLARATIVE_BASE):

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    __tablename__ = "publisher"

    def __repr__(self):
        return f"Publisher id :{self.id} , name : {self.name}"

    @classmethod
    def get(
        cls,
        session: Session,
        id_list: List[int] = None,
        name_list: List[str] = None,
    ):

        query = session.query(cls)
        if id_list:
            query = query.filter(cls.id.in_(id_list))
        if name_list:
            query = query.filter(cls.name.in_(name_list))

        return query.all()
