# crud_simpel_revisi-5-flask

Membuat query database :

CREATE TABLE categories (
	id_category CHAR(4) PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description TEXT
)

CREATE TABLE authors (
	id_author CHAR(4) PRIMARY KEY,
	name VARCHAR(255) NOT NULL, 
	nationality VARCHAR(255) NOT NULL, 
	year_birth INT NOT NULL
)

CREATE TABLE books (
	id_book SERIAL PRIMARY KEY,
	title VARCHAR(255) NOT NULL, 
	author VARCHAR(255) NOT NULL, 
	year INT NOT NULL, 
	total_pages INT NOT NULL, 
	category VARCHAR(255) NOT NULL,
	
	FOREIGN KEY (category) REFERENCES categories(id_category),
	FOREIGN KEY (author) REFERENCES authors(id_author)
)
