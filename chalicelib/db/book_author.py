import os
import sys
from typing import List

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Session

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)
from chalicelib.db.connector import DECLARATIVE_BASE
from chalicelib.db.author import Author
from chalicelib.db.book import Book

sys.path.remove(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)


class BookAuthorRelation(DECLARATIVE_BASE):

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)

    __tablename__ = "book_author"

    def __repr__(self):
        return f"Relation id : {self.id} , Book-id : {self.book_id} author-id {self.author_id}"

    @classmethod
    def get(
        cls,
        session: Session,
        id_list: List[int] = None,
        book_id_list: List[int] = None,
        author_id_list: List[int] = None,
    ):

        query = session.query(cls)
        if id_list:
            query = query.filter(cls.id.in_(id_list))
        if book_id_list:
            query = query.filter(cls.book_id.in_(book_id_list))
        if author_id_list:
            query = query.filter(cls.author_id.in_(author_id_list))

        return query.all()
