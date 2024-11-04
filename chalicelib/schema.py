import typing
import strawberry
from enum import Enum
from typing import Optional, List
from sqlalchemy.orm import Session
from strawberry.chalice.views import GraphQLView
from chalicelib.db.postgresql_connector import db
from chalicelib.db.author import Author as AuthorTable
from chalicelib.db.book import Book as BookTable
from chalicelib.db.book_author import BookAuthorRelation
from chalicelib.db.publisher import Publisher as PublisherTable


class MyGraphView(GraphQLView):

    def get_context(self, request, response):
        return {"session": db.session}


@strawberry.enum
class OrderDirection(Enum):
    ASC = "asc"
    DESC = "desc"


@strawberry.input
class OrderByInput:
    price: Optional[OrderDirection] = None


@strawberry.type
class Publisher:
    id: int
    name: str

    @strawberry.field
    def book(self, info) -> Optional[List["Book"]]:

        session: Session = info.context.get("session")
        result = []
        if session is not None:
            result = session.query(BookTable).filter(BookTable.id == self.id).all()
        return result


@strawberry.type
class Book:
    id: int
    title: str
    price: int
    publisher_id: int

    @strawberry.field(name="publisher")
    def publisher(self, info) -> Optional[Publisher]:
        session: Session = info.context.get("session")
        if session is not None:
            return (
                session.query(PublisherTable)
                .filter(PublisherTable.id == self.publisher_id)
                .first()
            )
        return None

    @strawberry.field(name="book_author")
    def book_author(self, info) -> Optional[List["BookAuthor"]]:
        session: Session = info.context.get("session")
        if session is not None:
            return (
                session.query(BookAuthorRelation)
                .filter(BookAuthorRelation.book_id == self.id)
                .all()
            )
        return None


@strawberry.type
class BookAuthor:
    id: int
    book_id: int
    author_id: int

    @strawberry.field(name="author")
    def author(self, info) -> Optional["Author"]:
        session: Session = info.context.get("session")
        if session is not None:
            return (
                session.query(AuthorTable)
                .filter(AuthorTable.id == self.author_id)
                .first()
            )
        return None

    @strawberry.field(name="book")
    def book(self, info) -> Optional["Author"]:
        session: Session = info.context.get("session")
        if session is not None:
            return session.query(BookTable).filter(BookTable.id == self.book_id).first()
        return None


@strawberry.type
class Author:
    id: int
    name: str
    age: str


@strawberry.type
class Query:

    @strawberry.field
    def book(
        self,
        ids: Optional[List[int]] = None,
        order_by: Optional[OrderByInput] = None,
    ) -> List[Book]:
        session = db.session
        result = BookTable.get(session=session, id_list=ids)
        if order_by:
            if order_by.price == OrderDirection.DESC:
                result.sort(key=lambda obj: obj.price, reverse=True)
            elif order_by.price == OrderDirection.ASC:
                result.sort(key=lambda obj: obj.price, reverse=False)

        return result

    @strawberry.field
    def publisher(
        self,
        ids: Optional[List[int]] = None,
    ) -> List[Publisher]:
        session = db.session
        publishers = PublisherTable.get(session=session, id_list=ids)
        result = []
        for publisher in publishers:
            result.append(Publisher(id=publisher.id, name=publisher.name))
        return result


@strawberry.type
class Mutation:

    @strawberry.mutation(name="insert_author_one")
    def insert_author_one(self, name: str, age: Optional[int] = None) -> Author:
        session = db.session
        obj = AuthorTable.create(session=session, name=name, age=age)
        return obj
