from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/task_library'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Books(db.Model):
    id_book = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    
    def __repr__(self) -> str:
        return f'Book {self.id_book} - {self.title}'
    
    # def __repr__(self) -> str:
    #     return super().__repr__()

class Categories(db.Model):
    id_category = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

class Authors(db.Model):
    id_author = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    year_birth = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET'])
def view_books():
    # data = Books.query.all()
    # db.session.execute('SELECT * FROM books')
    data = db.session.query(
        Books.id_book,
        Books.title,
        Authors.name.label('author'),
        Books.year,
        Books.total_pages,
        Categories.name.label('category')
    ).join(Authors, Books.author == Authors.id_author).join(Categories, Books.category == Categories.id_category).order_by(Books.id_book.desc()).all()
    
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
        
    return {'books': books_list}

@app.route('/<int:id_book>', methods=['GET'])
def view_book(id_book):
    data = Books.query.filter_by(id_book=id_book).first()
    print(data)
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
    data = Books(
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
    data = Books.query.filter_by(id_book=id_book).first()
    data.title = request.form['title']
    data.author = request.form['author']
    data.year = request.form['year']
    data.total_pages = request.form['total_pages']
    data.category = request.form['category']
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@app.route('/<int:id_book>', methods=['DELETE'])
def delete_book(id_book):
    data = Books.query.filter_by(id_book=id_book).first()
    db.session.delete(data)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)
