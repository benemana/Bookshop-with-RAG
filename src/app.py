import streamlit as st
import requests 
import pandas as pd
from db_queries.books import get_book


BASE_URL = "http://127.0.0.1:8000" 

#Funzioni helper per interagire con il backend
def list_books():
    response = requests.get(f"{BASE_URL}/books/api/manage")
    return response.json()["books"]

def add_book(title, author, genre, price, description, date):
    response = requests.post(f"{BASE_URL}/books/api/manage", json={"title": title, 
                                                                   "author": author,
                                                                   "genre": genre,
                                                                   "price": price,
                                                                   "description": description,
                                                                   "date": date})
    return response.json()["book_id"]

def update_book(id, title, author, genre, price, description, date):
    response = requests.put(f"{BASE_URL}/books/api/manage", json={"book_id": id,
                                                                       "title": title, 
                                                                       "author": author,
                                                                       "genre": genre,
                                                                       "price": price,
                                                                       "description": description,
                                                                       "date": date})
    
    #return response.json()["book"]

def delete_book(title):
    response = requests.delete(f"{BASE_URL}/books/api/manage?title={title}")
    return response.status_code

#UI Streamlit
def main():
    st.title("Gestione Libreria")

    operation = st.sidebar.selectbox("Seleziona Operazione", ["Lista Libri", "Aggiungi Libro", "Modifica Libro", "Rimuovi Libro", "Consigliami un libro"])

    if operation == "Lista Libri":
        books = list_books()
        if books:
            books_df = pd.DataFrame(books, columns=["title", "author", "date", "description", "price", "genre"])

            # Opzioni di ordinamento
            sort_option = st.selectbox("Ordina i libri per:", ["Prezzo crescente", "Prezzo decrescente", "Titolo", "Data", "Autore"])
            if sort_option == "Prezzo crescente":
                books_df = books_df.sort_values(by="price", ascending=True)
            elif sort_option == "Prezzo decrescente":
                books_df = books_df.sort_values(by="price", ascending=False)
            elif sort_option == "Titolo":
                books_df = books_df.sort_values(by="title", ascending=True)
            elif sort_option == "Data":
                books_df = books_df.sort_values(by="date", ascending=True)
            elif sort_option == "Autore":
                books_df = books_df.sort_values(by="author", ascending=True)
            
            # Filtri
            filter_genre = st.multiselect("Filtra per genere:", options=books_df["genre"].unique())
            filter_author = st.multiselect("Filtra per autore:", options=books_df["author"].unique())


            if filter_genre:
                books_df = books_df[books_df['genre'].isin(filter_genre)]
            if filter_author:
                books_df = books_df[books_df['author'].isin(filter_author)]
            
            if not books_df.empty:
                st.dataframe(books_df)
            else:
                st.write("Nessun libro trovato con i criteri specificati.")
        else:
            st.write("Nessun libro trovato.")

    elif operation == "Aggiungi Libro":
        title = st.text_input("Titolo del libro")
        author = st.text_input("Autore del libro")
        genre = st.text_input("Genere del libro")
        price = st.text_input("Prezzo del libro")
        description = st.text_input("Descrizione del libro")
        date = st.text_input("Data di pubblicazione del libro")

        if st.button("Aggiungi Libro"):
            if add_book(title, author, genre, price, description, date):
                st.success("Libro aggiunto con successo!")
            else:
                st.error("Errore durante l'aggiunta del libro.")

    elif operation == "Modifica Libro":
        books = list_books()
        books_dict = {book[0]: idx for idx, book in enumerate(books)}
        selected_book_title = st.selectbox("Seleziona il libro da modificare", options=list(books_dict.keys()))
        
        if selected_book_title:
            selected_book_id = books_dict[selected_book_title]
            book_details = books[selected_book_id]
            
            # Memorizza i dettagli del libro in session_state se non sono già presenti o se un nuovo libro è stato selezionato
            if 'selected_book' not in st.session_state or st.session_state.selected_book_id != selected_book_id:
                st.session_state.selected_book_id = selected_book_id
                st.session_state.title = book_details[0]
                st.session_state.author = book_details[1]
                st.session_state.date = book_details[2]
                st.session_state.description = book_details[3]
                st.session_state.price = book_details[4]
                st.session_state.genre = book_details[5]
                
                            
            title = st.text_input("Nuovo titolo", value=st.session_state.title)
            author = st.text_input("Nuovo autore", value=st.session_state.author)
            price = st.text_input("Prezzo del libro", value=st.session_state.price)
            description = st.text_input("Descrizione del libro", value=st.session_state.description)
            date = st.text_input("Data di pubblicazione del libro", value=st.session_state.date)
            genre = st.text_input("Genere del libro", value=st.session_state.genre)

            if st.button("Modifica Libro"):
                update_book(selected_book_id, title, author, genre, price, description, date)
                st.success("Libro modificato con successo!")
                del st.session_state['selected_book_id']
                del st.session_state['title']
                del st.session_state['author']
                del st.session_state['price']
                del st.session_state['description']
                del st.session_state['date']
                del st.session_state['genre']


    elif operation == "Rimuovi Libro":
        title = st.text_input("Titolo del libro da rimuovere")
        if st.button("Rimuovi Libro"):
            delete_book(title)
            st.success("Libro rimosso con successo!")
    
    elif operation == "Consigliami un libro":
        st.write("Clicca il pulsante per ricevere un consiglio su un libro da leggere.")
        preferences = st.text_input("Cosa vorresti leggere?")
        if st.button("Consigliami un libro"):
            response = requests.get(f"{BASE_URL}/books/api/recommend?preferences={preferences}")
            st.write(response.json()["books"])


if __name__ == "__main__":
    main()
