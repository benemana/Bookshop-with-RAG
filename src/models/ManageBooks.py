from db_queries.books import *

class Library():
    def __init__(self) -> None:
        pass
    
    def insert_book(self, book):
        """Insert a new book"""
        return insert_book(book)
    
    def get_books(self):
        """Get all books"""
        return get_books()
    
    def get_book(self, book_id):
        """Get a book"""
        return get_book(book_id)
    
    def update_book(self, book):
        """Update a book"""
        return update_book(book)
    
    def delete_book(self, title):
        """Delete a book"""
        return delete_book(title)
    

