from flask import Flask, jsonify

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

app.run(port=5000)

