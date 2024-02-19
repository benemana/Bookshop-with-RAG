from controllers.Controller import Controller
from models.ReccomendBooks import Suggester

class ReccomendBooks(Controller):
    def __init__(self,
                 method: str = 'GET',
                 header: dict = ...,
                 body: dict = ...,
                 params: dict = ...
                 ) -> None:
        super().__init__(method, header, body, params)

    def get(self) -> tuple:
        """Suggest a book"""
        user_preferences = self.params.get('preferences')
        suggester = Suggester()
        result = suggester.suggest_book(user_preferences)
        return {'books': result}, 200
    
    def post(self) -> tuple:
        return super().post()

    def put(self) -> tuple:
        return super().put()

    def delete(self) -> tuple:
        return super().delete()

