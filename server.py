from flask import Flask
from routes.books import books_routes

app = Flask(__name__)
app.register_blueprint(books_routes)

if __name__ == "__main__":
    app.run()

