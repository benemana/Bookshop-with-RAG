from abc import ABC, abstractmethod


class Controller(ABC):
    '''Controller'''

    def __init__(
        self, 
        method: str = 'GET', 
        header: dict = {}, 
        body: dict = {}, 
        params: dict = {}
                 ) -> None:
        self.method = method
        self.header = header
        self.body = body
        self.params = params

    def option(self) -> tuple:
        return '', 200

    def not_found(self) -> tuple:
        return '', 404

    @abstractmethod
    def post(self) -> tuple:
        self.not_found()

    @abstractmethod
    def get(self) -> tuple:
        self.not_found()

    @abstractmethod
    def delete(self) -> tuple:
        self.not_found()

    @abstractmethod
    def put(self) -> tuple:
        self.not_found()

    def api_manager(self) -> tuple:
        if self.method == 'OPTIONS':
            return self.option()
        elif self.method == 'POST':
            return self.post()
        elif self.method == 'GET':
            return self.get()
        elif self.method == 'DELETE':
            return self.delete()
        elif self.method == 'PUT':
            return self.put()
        else:
            return self.not_found()
