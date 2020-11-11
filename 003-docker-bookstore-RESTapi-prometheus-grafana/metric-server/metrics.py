from flask import Flask, abort, jsonify, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:talha123@database:3306/bookstore_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def number_of_books():
    query1 = '''
    SELECT COUNT(book_id) FROM books;
    '''
    result1 = db.session.execute(query1)
    count1 = ''.join(i for i in str(list(result1)) if i.isdigit())
    query2 = '''
    SELECT COUNT(DISTINCT author) FROM books;
    '''
    result2 = db.session.execute(query2)
    count2 = ''.join(i for i in str(list(result2)) if i.isdigit())
    return '''# HELP number_of_books test metrics\n# TYPE number_of_books gauge\nnumber_of_books{label="bookstore_application"} %d\n# HELP number_of_different_authors test metrics\n# TYPE number_of_different_authors gauge\nnumber_of_different_authors {label="bookstore_application"} %d''' %(int(count1), int(count2))

@app.route('/metrics', methods = ['GET'])
def metrics():
    response = make_response(number_of_books(), 200)
    response.mimetype = 'text/plain'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88)



