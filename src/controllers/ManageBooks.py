from controllers.Controller import Controller
from models.ManageBooks import Library

class ManageBooks(Controller):
    def __init__(self,
                 method: str = 'GET',
                 header: dict = ...,
                 body: dict = ...,
                 params: dict = ...
                 ) -> None:
        super().__init__(method, header, body, params)

    def post(self) -> tuple:
        """Insert a new book"""
        title = self.body.get('title')
        author = self.body.get('author')
        genre = self.body.get('genre')
        price = self.body.get('price')
        description = self.body.get('description')
        date = self.body.get('date')

        if not title or not author or not genre or not price or not description or not date:
            return {'error': 'Missing required fields'}, 400
        
        mng = Library()

        result = mng.insert_book({
            'title': title,
            'author': author,
            'genre': genre,
            'price': price,
            'description': description,
            'date': date
        })

        print(result)

        return {'book_id': result}, 201

    def get(self) -> tuple:
        """Get all books"""
        mng = Library()
        result = mng.get_books()
        return {'books': result}, 200

    def put(self) -> tuple:
        """Update a book"""
        book_id = self.body.get('book_id')
        title = self.body.get('title')
        author = self.body.get('author')
        genre = self.body.get('genre')
        price = self.body.get('price')
        description = self.body.get('description')
        date = self.body.get('date')
       
        mng = Library()

        result = mng.update_book({
            'bookId': book_id,
            'title': title,
            'author': author,
            'genre': genre,
            'price': price,
            'description': description,
            'date': date
        })
       
        if result == 0:
            return {'book': -1}, 404
        
        return {'book': result}, 204

    def delete(self) -> tuple:
        """Delete a book"""
        title = self.params.get('title')

        if not title:
            return {'error': 'Missing required fields'}, 400
        
        mng = Library()
        result = mng.delete_book(title)
        if result == 0:
            return {'error': 'Book not found'}, 404
        return {'result': result}, 204
