from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/technicalsuccessmanager/projects/books_api/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False