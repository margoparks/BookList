from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://booklist:readingrainbow@localhost:8889/booklist'
app.config['SQLALCHEMY_ECHO']= True
db = SQLAlchemy(app)
app.secret_key = 'be9{aM47/X'

class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    author= db.Column(db.String(120))
    completed = db.Column(db.Boolean, default = False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, author, owner):
        self.title =  title
        self.author = author
        self.completed = False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique = True)
    password = db.Column(db.String(60))
    books = db.relationship('Book', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        book = request.form['book_title']
        author = request.form['book_author']
        new_book = Book(book, author, owner)
        db.session.add(new_book)
        db.session.commit()

    books = Book.query.filter_by(completed = False, owner = owner).all()
    completed_books = Book.query.filter_by(completed = True, owner = owner).all()
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

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('login')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged In")
            return redirect('/')
        else:
            flash("User password is incorrect", "error")


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
            session['email'] = email  
            return redirect('/')
        else:
            # TODO - better error message for user 
            return '<h3> Duplicate User </h3>'


    return render_template('register.html', title="Register")

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

    

    
if __name__ == '__main__': 
    app.run()