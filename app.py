from chalice import Chalice
from chalice.app import Request, Response

import strawberry
from chalicelib.endpoint import get_author
from chalicelib.schema import Query, Mutation, MyGraphView


app = Chalice(app_name="demo")


schema = strawberry.Schema(query=Query, mutation=Mutation)
view = MyGraphView(schema=schema)


@app.route("/graphql", methods=["POST"], content_types=["application/json"])
def handle_graphql() -> Response:
    request: Request = app.current_request
    result = view.execute_request(request)
    return result


@app.middleware("http")
def parse_event(event, get_response):
    if event.query_params is None:
        event.query_string = {}
    else:
        event.query_string = dict(event.query_params)
    multi_value_query_string = event._event_dict.get("multiValueQueryStringParameters")
    if multi_value_query_string is None:
        event.multi_value_query_string = {}
    else:
        event.multi_value_query_string = multi_value_query_string
    return get_response(event)


@app.route("/author", methods=["GET", "PUT", "POST", "DELETE"])
def author():
    request = app.current_request
    method = app.current_request.method
    if method == "GET":
        return get_author(request)
