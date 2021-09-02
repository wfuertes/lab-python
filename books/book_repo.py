import logging
from books.book import Book
from contextlib import closing
from mysql.connector import Error


class BookRepository:

    def __init__(self, pool):
        self.pool = pool

    def findall(self):
        try:
            with closing(self.pool.get_connection()) as conn:
                with closing(conn.cursor(dictionary=True)) as book_cursor:
                    db_info = conn.get_server_info()
                    logging.info(f'Connected to MySQL Server version: {db_info}')

                    query = 'SELECT id, title, price FROM books'
                    book_cursor.execute(str(query))
                    books = list(map(Book.from_dict, book_cursor.fetchall()))
                    
                    return books
        except Error as err:
            logging.error(f'Error while connectiong to MySQL: {err}')
