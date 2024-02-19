from db_queries.books import *
import pandas as pd
import openai
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from config.config import Config
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import chroma
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from operator import itemgetter

OPENAI_API_KEY = Config.env.get('OPENAI_API_KEY')

class Suggester():
    def __init__(self) -> None:
        pass
    
    def get_books(self):
        """Get all books"""
        return get_books()
    
    def suggest_book(self, user_preferences):
        """Suggest a book"""
        books = self.get_books()

        books_df = pd.DataFrame(books, columns=["title", "author", "date", "description", "price", "genre"])
        books_df.columns = ["Title", "Author", "Date", "Description", "Price", "Genre"]

        books_df['combined_info'] = books_df.apply(lambda row: f"Title: {row['Title']}. Description: {row['Description']} Genres: {row['Genre']}", axis=1)

        rag_system = self.get_rag_system(books_df)

        question = user_preferences

        response = rag_system({'query': question})

        return response['result']

    def generate_book_embeddings(self, books_df):
        """Generate book embeddings"""
        df_loader = DataFrameLoader(books_df, page_content_column='combined_info')
        df_document = df_loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=10)
        texts = text_splitter.split_documents(df_document)

        print(texts)

        embed_model = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY
        )

        vdb = chroma.Chroma.from_documents(texts, embed_model, persist_directory='./input')

        retriever = vdb.as_retriever()

        return retriever
    
    def get_custom_prompt(self):
        template = """
        Sei un sistema di raccomandazione di libri che aiuta gli utenti a trovare libri in base alle loro preferenze.
        Data questa richiesta dell'utente: 
        {question}
        Seleziona un libro, scegliendolo solo ed esclusivamente tra quelli menzionati nel seguente contesto, selezionando il più appropriato a soddisfare la richiesta dell'utente:
        {context}
        Per il libro scelto, indica chiaramente il suo titolo, che nel contesto fornito è sempre preceduto dalla parola 'Title:', poi fornisci una descrizione riassuntiva del libro basandoti solo sul contesto fornito in precedenza, e infine indica il motivo per cui potrebbe piacere all'utente.
        Se non conosci la risposta, semplicemente dì che non lo sai, non cercare di inventare una risposta.

        Struttura la tua risposta nel seguente modo:
        - Titolo: [titolo del libro]
        - Descrizione: [descrizione riassuntiva del libro]
        - Perchè potrebbe piacerti: [motivi per cui potrebbe piacere all'utente]

        Nella tua riposta, dai del tu all'utente e usa un linguaggio informale.
        """

        #prompt = PromptTemplate(input_variables=['context', 'question'], template=template)

        prompt = PromptTemplate.from_template(template)

        chain_type_kwargs = {"prompt": prompt}

        return chain_type_kwargs
    
    def get_rag_system(self, df_books):

        llm = ChatOpenAI(
            model_name='gpt-3.5-turbo',
            temperature=0,
            openai_api_key = OPENAI_API_KEY)
        
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=self.generate_book_embeddings(df_books),
            return_source_documents=True,
            chain_type_kwargs=self.get_custom_prompt()
        )

        return qa


    

