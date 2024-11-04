from chalicelib.db.connector import PsqlConnector

db = PsqlConnector(
    username="postgres",
    password="postgrespassword",
    host="localhost",
    port="5433",
    db_name="postgres",
    echo=True,
)
