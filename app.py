from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        'name' : 'Green Eggs and Ham',
        'price' : 7.99,
        'isbn' : 978039400165
    },
    {
        'name' : 'The Cat In The Hat',
        'price' : 6.99,
        'isbn' : 978237100193
    }
]


#GET /books
@app.route('/books')
def get_books():
    return jsonify({'books' : books})

def validBookObject(bookObject):
    if('name' in bookObject and 'price' in bookObject and 'isbn' in bookObject):
        return True
    else:
        return False

@app.route('/books', methods=['POST'])
def add_book():
    request_data = jsonify(request.get_json())
    if(validBookObject(request_data)):
        new_book = {
            'name' : request_data['name'],
            'price' : request_data['price'],
            'isbn' : request_data['isbn']
        }
        books.insert(0, new_book)
        return 'True'
    else:
        return 'False'

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name' : book['name'],
                'price' : book['price']
            }
    return jsonify(return_value)

app.run(port=5000)

