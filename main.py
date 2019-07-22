from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('bookForm.html')

@app.route("/hello", methods=['POST'])
def hello():
    book_title = request.form['book_title']
    return '<h1> Enjoy reading ' + book_title + '! </h1>'

    
    
app.run()