import mysql.connector
from mysql.connector import errorcode
import time

config = {
    'user': 'talha-01',
    'password': 'phonebook_123',
    'host': 'database',
    'database':'phonebook',
    'raise_on_warnings': True
}

def init_phone_book_db(cursor):
    # drop_table = 'DROP TABLE IF EXISTS phone_book;'
    phone_book_table = '''
    CREATE TABLE phone_book(
        id INTEGER NOT NULL AUTO_INCREMENT,
        name varchar(50) NOT NULL,
        number varchar(13),
        PRIMARY KEY(`id`)
    ) ENGINE=InnoDB;
    '''
    data = '''
    INSERT INTO phone_book (id, name, number)
    VALUES
    (1, 'John Doe', '(555)999-6644'),
    (2, 'Jane Doe', '(555)888-4455');
    '''
    # cursor.execute(drop_table)
    cursor.execute(phone_book_table)
    cursor.execute(data)
db_not_ready = True
while db_not_ready:
    try:
        connection = mysql.connector.connect(**config)
        init_phone_book_db(connection.cursor(buffered = True))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something went wrong with the username or password')
            time.sleep(3)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
            time.sleep(3)
        elif err.errno == 2003:
            print('mysql server is not ready')
            time.sleep(3)
        elif err.errno == 1050:
            print('There is already a table with the same name')
            db_not_ready = False
            connection.close()
        else:
            print(f'error is {err.errno} and {errorcode}')
            time.sleep(3)
    else:
        print('phone_book table created successfully')
        db_not_ready = False
        connection.close()



