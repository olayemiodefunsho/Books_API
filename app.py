from flask import Flask, jsonify, request, Response, json
from BookModel import *
from settings import *
import json
import jwt, datetime

app.config['SECRET_KEY'] = 'meow'

def validBookObject(bookObject):
    if('name' in bookObject and 'price' in bookObject and 'isbn' in bookObject):
        return True
    else:
        return False

@app.route('/login')
def get_token():
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp' : expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
    return token

#GET /books
@app.route('/books')
def get_books():
    token = request.args.get('token')
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return jsonify({'error': 'Need a valid token to view this page'}), 401
    return jsonify({'books' : Book.get_all_books()})

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()

    if(validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            'error' : 'Invalid book object passed in request',
            'helpstring' : "Data passed in similar to this {'name':'bookname', 'price':'7.99', 'isbn':123213213312}"

        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), 400, mimetype='application/json')
        return response

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    Book.replace_book(isbn, request_data["name"], request_data["price"])
    response = Response('', status=204)
    return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if('name' in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if('price' in request_data):
        Book.update_book_price(isbn, request_data['price'])
        
    response = Response('', status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response('', status=204)
        return response

    invalidBookObjectErrorMsg = {
        'error' : 'Invalid book object passed in request'
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), 404, mimetype='application/json')
    return response


app.run(port=5000)

