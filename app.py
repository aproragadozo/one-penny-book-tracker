from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
import re
# this is causing a circular import, and probably won't be needed
# from scraper import get_price, run

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# connecting to postgres instead of sqlite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
# replacing postgres with postgresql with postgres in vercel's postgres url variable
db_url = re.sub(pattern="^postgres$", repl="postgresql", string=os.environ.get('POSTGRES_URL'))
# using the new replaced uri
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "super-secret" # change this and store with gitguardian
#using mailtrap.io for now; basically Postman for email
app.config["MAIL_SERVER"] = "sandbox.smtp.mailtrap.io"
#app.config["MAI_USERNAME"] = os.environ["MAIL_USERNAME"]
#app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '428f7eed3c0d77'
app.config['MAIL_PASSWORD'] = 'c7235b60a86dd1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

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

# routes

@app.route('/')
def home():
    #return jsonify(message="Hello World!"), 200
    return render_template("index.html")

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

@app.route('/users', methods=["GET"])
def users():
    user_list = User.query.all()
    result = users_schema.dump(user_list)
    return jsonify(result)

@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    # see if user already exists
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message="That email already exists."), 409
        # add new user
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully"), 201

@app.route("/login", methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login successful", access_token=access_token)
    else:
        return jsonify(message="Wrong email or password"), 401

@app.route("/retrieve_password/<string:email>", methods=["GET"])
def retrieve_password(email:str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("your password is " + user.password, sender="admin@one-penny.com", recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist."), 401

@app.route("/book_details/<int:book_id>", methods=["GET"])
def book_details(book_id:int):
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        result = book_schema.dump(book)
        return jsonify(result)
    else:
        return jsonify(message="That book doesn't exist in the database.")

@app.route("/add_book", methods=["POST"])
def add_book():
    isbn = request.form["isbn"]
    # see if book already exists
    test = Book.query.filter_by(isbn=isbn).first()
    if test:
        return jsonify(message="This book is already part of the database."), 409
    else:
        new_book = Book(title=request.form["title"], author=request.form["author"], isbn=isbn, price=get_price(f"https://amazon.co.uk/dp/{isbn}"))
        db.session.add(new_book)
        db.session.commit()
        return jsonify(message="New book record created."), 201


# trigger scraper
@app.route("/trigger", methods=["GET", "POST"])
def trigger_scraper():
    run()


# database models
# commenting User out for now
# class User(db.Model):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     email = Column(String, unique=True)
#     password = Column(String)

# postgres model
class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    current_lowest_price = db.Column(db.Float, nullable=False)
    link = db.Column(db.String(500), nullable=False)

# create the books table
with app.app_context():
    db.create_all()
# marshmallow classes
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "password")

class BookSchema(ma.Schema):
    class Meta:
        fields= ("book_id", "title", "author", "current_lowest_price", "link")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)