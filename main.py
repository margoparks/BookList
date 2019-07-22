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

    def __init__(self, title, author):
        self.title =  title
        self.author = author

books= []


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        book = request.form['book_title']
        books.append(book)

    return render_template('bookForm.html', title="BookList", books=books)


    
if __name__ == '__main__': 
    app.run()