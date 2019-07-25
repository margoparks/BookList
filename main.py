from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://booklist:readingrainbow@localhost:8889/booklist'
app.config['SQLALCHEMY_ECHO']= True
db = SQLAlchemy(app)

class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    author= db.Column(db.String(120))
    completed = db.Column(db.Boolean, default = False)

    def __init__(self, title, author):
        self.title =  title
        self.author = author
        self.completed = False

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique = True)
    password = db.Column(db.String(60))

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        book = request.form['book_title']
        author = request.form['book_author']
        new_book = Book(book, author)
        db.session.add(new_book)
        db.session.commit()

    books = Book.query.filter_by(completed = False).all()
    completed_books = Book.query.filter_by(completed = True).all()
    return render_template('bookForm.html', 
    title="BookList", books=books, completed_books = completed_books)


@app.route('/remove-book', methods=['POST'])
def remove_book():
    book_id = int(request.form['book-id'])
    book = Book.query.get(book_id)
    book.completed = True
    db.session.add(book)
    db.session.commit()

    return redirect('/')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.password == password:
            # TODO - remember the user has logged in with session
            return redirect('/')
        else:
            # TODO explain why login has failed
            pass
            return '<h3> Error </h3>'


    return render_template('login.html', title="Log In")

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        #TODO - validate user's info
        existing_user = user = User.query.filter_by(email = email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            # TODO remember the new user with sessions
            return redirect('/')
        else:
            # TODO - better error message for user
            return '<h3> Duplicate User </h3>'


    return render_template('register.html', title="Register")


    

    
if __name__ == '__main__': 
    app.run()