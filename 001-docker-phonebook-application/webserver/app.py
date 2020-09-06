from flask import Flask, abort, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
# 'mysql+pymysql://admin_1:Admin_123@phonebook.c7s3y2m1dquv.us-west-2.rds.amazonaws.com:3306/phone_book'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://talha-01:phonebook_123@database:3306/phonebook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def insert_person(name, number):
    insert = f'''
    INSERT INTO phone_book (name, number)
    VALUES ('{name}', '{number}');
    '''
    result = db.session.execute(insert)
    db.session.commit()

def remove_person(name):
    delete = f'''
    DELETE FROM phone_book
    WHERE id=(SELECT * FROM (SELECT id FROM phone_book WHERE name='{name}') as t);
    '''
    result = db.session.execute(delete)
    db.session.commit()

def search_person(word):
    query = f'''
    SELECT * FROM phone_book
    WHERE name LIKE '%{word}%';
    '''
    result = db.session.execute(query)
    persons = [{'id':row[0], 'name':row[1], 'number':row[2]} for row in result]
    return persons

def find_person(word):
    query = f'''
    SELECT * FROM phone_book
    WHERE name LIKE '{word}';
    '''
    result = db.session.execute(query)
    persons = [{'id':row[0], 'name':row[1], 'number':row[2]} for row in result]
    return persons

def bring_em_all():
    query = '''
    SELECT * FROM phone_book;
    '''
    result = db.session.execute(query)
    persons = [{'id':row[0], 'name':row[1], 'number':row[2]} for row in result]
    return persons

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html', developer_name = 'Talha', show_result = False)
    if request.method == 'POST':
        keyword = request.form['username']
        if not keyword.strip():
            return render_template('index.html', developer_name = 'Talha', show_result = False)
        persons = search_person(keyword.title())
        if persons:
            return render_template('index.html', developer_name = 'Talha', show_result = True, keyword = keyword, persons = persons, no_result = False)
        else:
            return render_template('index.html', developer_name = 'Talha', show_result = False, keyword = keyword, persons = persons, no_result = True)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add-update.html', developer_name = 'Talha', action_name = 'Add', not_valid = False, show_result = False)
    if request.method == 'POST':
        name = request.form['username']
        if not name.replace(' ', '').isalpha():
            errors = ['Name cannot be empty.', 'Name of person should be text.']
            return render_template('add-update.html', developer_name = 'Talha', action_name = 'Add', not_valid = True, message = f'Invalid input: {errors[bool(name.strip())]}', show_result = False)

        number = request.form['phonenumber']
        if not number.isdecimal() or not len(number) == 10:
            errors = ['Phone number can not be empty.', 'Phone number should be a number and consist of 10 digits.']
            return render_template('add-update.html', developer_name = 'Talha', action_name = 'Add', not_valid = True, message = f'Invalid input: {errors[bool(name.strip())]}', show_result = False)
        name = name.title()
        number = f'({number[:3]}){number[3:6]}-{number[6:]}'
        insert_person(name, number)
        result = find_person(name)
        return render_template('add-update.html', developer_name = 'Talha', action_name = 'Add', not_valid = False, show_result = True, result = f"{result[0]['name']} ---- {result[0]['number']}")

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('add-update.html', developer_name = 'Talha', action_name = 'Update', not_valid = False, show_result = False)
    if request.method == 'POST':
        name = request.form['username']
        if not name.replace(' ', '').isalpha():
            errors = ['Name cannot be empty.', 'Name of person should be text.']
            return render_template('add-update.html', developer_name = 'Talha', action_name = 'Update', not_valid = True, message = f'Invalid input: {errors[bool(name.strip())]}', show_result = False)
        if not find_person(name):
            return render_template('add-update.html', developer_name = 'Talha', action_name = 'Update', not_valid = True, message = f"No record found for '{name}'", show_result = False)
        number = request.form['phonenumber']
        if not number.isdecimal():
            errors = ['Phone number can not be empty.', 'Phone number should be a number and consist of 10 digits.']
            return render_template('add-update.html', developer_name = 'Talha', action_name = 'Update', not_valid = True, message = f'Invalid input: {errors[bool(name.strip())]}', show_result = False)
        name = name.title()
        remove_person(name)
        number = f'({number[:3]}){number[3:6]}-{number[6:]}'
        insert_person(name, number)
        result = find_person(name)
        return render_template('add-update.html', developer_name = 'Talha', action_name = 'Update', not_valid = False, show_result = True, result = f"{result[0]['name']} ---- {result[0]['number']}")


@app.route('/delete', methods = ['GET','POST'])
def remove():
    if request.method == 'GET':
        return render_template('delete.html', developer_name = 'Talha', not_valid = False, show_result = False)
    if request.method == 'POST':
        name = request.form['username']
        if not name.replace(' ', '').isalpha():
            errors = ['Name cannot be empty.', 'Name of person should be text.']
            return render_template('delete.html', developer_name = 'Talha', not_valid = True, message = f'Invalid input: {errors[bool(name.strip())]}', show_result = False)
        name = name.title()
        if not find_person(name):
            return render_template('delete.html', developer_name = 'Talha', not_valid = True, message = f'No record found for {name}', show_result = False)
        remove_person(name)
        result = f'{name} not deleted !' if find_person(name) else f'{name} deleted !'
        return render_template('delete.html', developer_name = 'Talha', not_valid = False, show_result = True, result = result)

@app.route('/test', methods = ['GET'])
def whole_list():
    return jsonify({'contacts':bring_em_all()})

if __name__ == '__main__':
    # init_phone_book_db()
    app.run('0.0.0.0', port=5000)