from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def home():
    return jsonify(message="Hello World!"), 200
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# database scripts
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Database created")

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database dropped")

@app.cli.command('db_seed')
def db_seed():
    test_user = User(first_name="Alma", last_name="Barack", email="aproragadozo@gmail.com", password="Alma123")
    test_book = Book(title="Aristotle Detective: Murder and Mystery in Ancient Athens", author="Margaret Doody", isbn="0099436132", price=1.10)
    
    db.session.add(test_book)
    db.session.add(test_user)
    db.session.commit()
    print("database seeded")

@app.route('/not_found')
def not_found():
    return jsonify(message="That resource wasn't found."), 404

@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message=f"Sorry {name}, you aren't old enough."), 401
    else:
        return jsonify(message=f"Welcome {name}!")


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name:str, age:int):
    if age < 18:
        return jsonify(message=f"Sorry {name}, you aren't old enough."), 401
    else:
        return jsonify(message=f"Welcome {name}!")

@app.route('/books', methods=["GET"])
def books():
    book_list = Book.query.all()
    result = books_schema.dump(book_list)
    return jsonify(result)


# database models
class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Book(db.Model):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String, unique=True)
    price = Column(Float)

# marshmallow classes
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "password")

class BookSchema(ma.Schema):
    class Meta:
        fields= ("title", "author", "isbn", "price")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

if __name__ == '__main__':
    app.run()