from chalicelib.db.postgresql_connector import db
from chalicelib.db.author import Author


def get_author(request):
    session = db.session
    parameter_in_list = request.multi_value_query_string
    author_id_list = parameter_in_list.get("id", [])
    authors = Author.get(session=session, id_list=author_id_list)
    result = []
    for author in authors:
        result.append({"id": author.id, "name": author.name, "age": author.age})
    return result
