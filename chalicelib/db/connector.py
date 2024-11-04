from typing import List

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy.pool import NullPool


def to_dict(self):
    d = {}
    for c in self.__table__.columns:
        d[c.name] = getattr(self, c.name, None)
    return d


DECLARATIVE_BASE = declarative_base()
DECLARATIVE_BASE.to_dict = to_dict


class Connector:
    def __init__(
        self,
        engine_url: str,
        echo: bool = False,
    ) -> None:
        self.echo = echo
        self.engine_url = engine_url
        self.engine = self._create_engine(self.engine_url, self.echo)
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))
        self.session = self.session_factory()

        def to_dict(self):
            d = {}
            for c in self.__table__.columns:
                d[c.name] = getattr(self, c.name, None)
            return d

        self.base = declarative_base()
        self.base.to_dict = to_dict

    def _create_engine(self, url, echo):
        engine = create_engine(url, echo=echo, pool_pre_ping=True, poolclass=NullPool)
        # base.metadata.create_all(engine)
        return engine


class PsqlConnector(Connector):
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        db_name: str,
        echo: bool = False,
    ) -> None:
        """
        Please check sqlalchemy docs for parameter settings:
            https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine

        Usage:
            sql_connector = PostgreSqlConnector(...)
            session = sql_connector.session # create the session
        """
        engine_url = "postgresql://{}:{}@{}:{}/{}".format(
            username,
            password,
            host,
            port,
            db_name,
        )
        super().__init__(engine_url=engine_url, echo=echo)
        self.base = DECLARATIVE_BASE

    def create_tables(self):
        self.base.metadata.create_all(self.engine)

    def drop_tables(self):
        self.base.metadata.drop_all(self.engine)

    def get_table_list(self) -> List[str]:
        """return all of the table names in the database"""
        inspector = inspect(self.engine)
        table_list = [table for table in inspector.get_table_names()]
        return table_list

    def get_connection_pool_status(self) -> str:
        """get status of the connection pool for debug usage"""
        return self.engine.pool.status()

    def check_table_exists(self, table_name: str) -> bool:
        """check if a specific table exists or not, return True if the table exists"""
        return inspect(self.engine).has_table(table_name)
