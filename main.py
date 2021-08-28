import csv
import io
import configparser
import mysql.connector
from flask import Flask, json
from mysql.connector import Error

api = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

def find_books():
    try:
        with mysql.connector.connect(
            host=config['MySQL']['host'],
            database=config['MySQL']['database'],
            user=config['MySQL']['username'],
            password=config['MySQL']['password']
        ) as connection:
            with connection.cursor() as cursor:
                db_info = connection.get_server_info()
                print(f'Connected to MySQL Server version: {db_info}')

                cursor = connection.cursor()
                cursor.execute('SELECT id,title,price FROM books')
                result = list(
                    map(
                        lambda v: {'id': v[0], 'title': v[1],
                                   'price': float(v[2])},
                        cursor.fetchall()
                    )
                )
                return result
    except Error as err:
        print(f'Error while connectiong to MySQL: {err}')

@api.route('/books', methods=['GET'])
def get_books():
    return json.dumps(find_books()), 200, {'Content-Type': 'application/json; charset=utf-8'}

@api.route('/books/csv', methods=['GET'])
def get_books_csv():
    books = find_books()
    fields = ['id', 'title', 'price']
    rows = list(map(lambda v: (v['id'], v['title'], v['price']), books))

    with io.StringIO() as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
        return f.getvalue(), 200, {'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': 'attachment; filename="books.csv"'}

if __name__ == '__main__':
    api.run()

# List of books as input
# try:
#     connection = mysql.connector.connect(
#         host="localhost", database="library", user="root", password="root")

#     db_info = connection.get_server_info()
#     print(f'Connected to MySQL Server version: {db_info}')

#     cursor = connection.cursor()
#     cursor.execute('SELECT id,title,price FROM books')
#     record = cursor.fetchall()
#     print(f'Record found: {record}')

# except Error as err:
#     print(f'Error while connectiong to MySQL: {err}')
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print('MySQL connection is closed')


# # Open a file to write the content
# with open('books.csv', 'w') as csv_file:
#     writer = csv.writer(csv_file)
#     for k, v in input_books.items():
#         writer.writerow([k, v])

# # Reading from file
# with open('books.csv') as csv_file:
#     reader = csv.reader(csv_file)
#     books = dict(reader)

# # Just printing the read elements
# print(books)
