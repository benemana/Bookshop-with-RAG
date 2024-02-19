from config.db import OpenDBconnection

def get_books():
    with OpenDBconnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT title, author, date, description, price, genre FROM books")
            return cursor.fetchall()

def get_book(book_id):
    with OpenDBconnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT title, author, date, description, price FROM books WHERE book_id = %s", (book_id,))
            return cursor.fetchone()
        
def insert_book(book):
    with OpenDBconnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO books (title, author, genre, price, description, date) VALUES (%s, %s, %s, %s, %s, %s)", (book['title'], book['author'], book['genre'], book['price'], book['description'], book['date']))
            conn.commit()
            return cursor.lastrowid
        
def update_book(book):
    with OpenDBconnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE books SET author = %s, genre = %s, price = %s, description = %s, date = %s WHERE title = %s", (book['author'], book['genre'], book['price'], book['description'], book['date'], book['title']))
            conn.commit()
            return cursor.rowcount
        
def delete_book(book_title):
    with OpenDBconnection() as conn:
        with conn.cursor() as cursor:
            query = "DELETE FROM books WHERE title = %s"
            cursor.execute(query, (book_title,))
            conn.commit()
            return cursor.rowcount

