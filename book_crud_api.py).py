from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database
books = []
next_id = 1

# Create a new book (POST)
@app.route('/books', methods=['POST'])
def create_book():
    global next_id
    data = request.json
    if not data or 'book_name' not in data or 'author' not in data or 'publisher' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    new_book = {
        'id': next_id,
        'book_name': data['book_name'],
        'author': data['author'],
        'publisher': data['publisher']
    }
    books.append(new_book)
    next_id += 1
    return jsonify(new_book), 201

# Read all books (GET)
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# Read a single book by ID (GET)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book), 200

# Update a book by ID (PUT)
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    book['book_name'] = data.get('book_name', book['book_name'])
    book['author'] = data.get('author', book['author'])
    book['publisher'] = data.get('publisher', book['publisher'])
    return jsonify(book), 200

# Delete a book by ID (DELETE)
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    books = [b for b in books if b['id'] != book_id]
    return jsonify({'message': 'Book deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
