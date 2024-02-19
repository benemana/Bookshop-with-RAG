from controllers.ManageBooks import ManageBooks
from flask import request, Blueprint
from classes.Service import HTTP_Header
from controllers.ReccomendBooks import ReccomendBooks


books_routes = Blueprint('books_routes', __name__,
                          url_prefix="/books/api/")

@books_routes.route("/manage", methods=['OPTIONS', 'GET', 'POST', 'PUT', 'DELETE'])
def manage_books() -> tuple:

    try:
        body = request.get_json()
    except:
        body = {}

    params = request.args if request.args is not None else {}

    header = request.headers if request.headers is not None else {}

    Controller = ManageBooks(method=request.method,
                                  params=params, header=header, body=body)

    data, status = Controller.api_manager()

    return data, status, HTTP_Header

@books_routes.route("/recommend", methods=['OPTIONS', 'GET'])
def reccomend_books() -> tuple:
    try:
        body = request.get_json()
    except:
        body = {}

    params = request.args if request.args is not None else {}

    header = request.headers if request.headers is not None else {}

    Controller = ReccomendBooks(method=request.method,
                                  params=params, header=header, body=body)

    data, status = Controller.api_manager()

    return data, status, HTTP_Header