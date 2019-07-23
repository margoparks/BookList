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

    

    
if __name__ == '__main__': 
    app.run()