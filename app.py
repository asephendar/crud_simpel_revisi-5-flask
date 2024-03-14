from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/task_library'
db = SQLAlchemy(app)

class books(db.Model):
    id_book = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=False)

@app.route('/', methods=['GET'])
def view_books():
    data = books.query.all()
    books_list = []
    
    for el in data:
        books_list.append({
            'id_book': el.id_book,
            'title': el.title,
            'author': el.author,
            'year': el.year,
            'total_pages': el.total_pages,
            'category': el.category
        })
        
    return jsonify({'books': books_list})

@app.route('/<int:id_book>', methods=['GET'])
def view_book(id_book):
    data = books.query.filter_by(id_book=id_book).first()
    book_data = {
        'id_book': data.id_book,
        'title': data.title,
        'author': data.author,
        'year': data.year,
        'total_pages': data.total_pages,
        'category': data.category
    }
        
    return jsonify({'book': book_data})

@app.route('/', methods=['POST'])
def add_book():
    data = books(
        title = request.form['title'],
        author = request.form['author'],
        year = request.form['year'],
        total_pages = request.form['total_pages'],
        category = request.form['category']
    )
    db.session.add(data)
    db.session.commit()
    return jsonify({'message': 'Book added'})

@app.route('/<int:id_book>', methods=['PUT'])
def update_book(id_book):
    data = books.query.filter_by(id_book=id_book).first()
    data.title = request.form['title']
    data.author = request.form['author']
    data.year = request.form['year']
    data.total_pages = request.form['total_pages']
    data.category = request.form['category']
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@app.route('/<int:id_book>', methods=['DELETE'])
def delete_book(id_book):
    data = books.query.filter_by(id_book=id_book).first()
    db.session.delete(data)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)
