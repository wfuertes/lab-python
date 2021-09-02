import io
import csv
import logging
import configparser
from books.book import Book
from flask import Flask, json
from mysql.connector import pooling
from books.book_repo import BookRepository
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

config = configparser.ConfigParser()
config.read('config.ini')

pool = pooling.MySQLConnectionPool(pool_name='mysql', pool_size=5, pool_reset_session=True, **config['MySQL'])
book_repo = BookRepository(pool)

class JsonMapper(json.JSONEncoder):
    def default(self, obj):
        if (hasattr(obj, 'to_dict')):
            return obj.to_dict()
        else:
            return super().default(obj)

# Declaring Flask App routes
api = Flask(__name__)

@api.route('/books', methods=['GET'])
def get_books():
    books = book_repo.findall()
    return json.dumps(books, cls=JsonMapper), 200, {'Content-Type': 'application/json; charset=utf-8'}

@api.route('/books/csv', methods=['GET'])
def get_books_csv():
    books = book_repo.findall()
    rows = list(map(lambda book: book.to_tuple(), books))

    with io.StringIO() as output:
        write = csv.writer(output)
        write.writerow(Book.fields())
        write.writerows(rows)
        return output.getvalue(), 200, {'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': 'attachment; filename="books.csv"'}

# Extending RequestHandler in order to support logs
class WithLoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        logging.info(format % args)

    def log_error(self, format, *args):
        logging.error(format % args)

# Bootstraping the App Server
with make_server(host='', port=5000, app=api, server_class=WSGIServer, handler_class=WithLoggingWSGIRequestHandler) as httpd:
    logging.info('Server is running on port: 5000')
    httpd.serve_forever()
