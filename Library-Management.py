import mysql.connector
from datetime import datetime, timedelta


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="LibraryDB"

)

if conn.is_connected():
    print("Connection successful!")
    db_info = conn.get_server_info()
    print("Connected to MySQL server version",db_info)
else:
    print("Connection failed!")


cursor = conn.cursor()

def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
                   book_id INT AUTO_INCREMENT PRIMARY KEY,
                   title VARCHAR(255),
                   author VARCHAR(255),
                   genre VARCHAR(100),
                   publish_year INT,
                   availability BOOLEAN DEFAULT TRUE
                   );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Members(
                   membre_id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(255),
                   contact_info VARCHAR(255)
                   );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions(
                   transactions_id INT AUTO_INCREMENT PRIMARY KEY,
                   member_id INT,
                   book_id INT,
                   borow_date DATE,
                   return_date DATE,
                   due_date DATE,
                   FOREIGN KEY (member_id) REFERENCES members(member_id),
                   FOREIGN KEY (book_id) REFERENCES Books(book_id)

                   ); 

    ''')


def add_book(title,author,genre,publish_year):
    cursor.execute('''
    INSERT INTO Books(title,author,genre,publish_year,availability)
    VALUES (%s, %s, %s, %s, %s)
    ''', (title,author,genre,publish_year,True))
    conn.commit()



def borrow_book(member_id,book_id):
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() +timedelta(days=15)).strftime("%Y-%m-%d")

    cursor.execute('''
    INSERT INTO Transactions(member_id, book_id, borrow_date, due_timw)
    VALUES (%s, %s, %s, %s)
    ''',(member_id,book_id,borrow_date,due_date))

    cursor.execute('UPDATE Books SET availability = %s WHERE book_id = %s', (False,book_id))
    conn.commit()


def return_book(transaction_id, book_id):
    return_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
    UPDATE Transactions SET return_date = %s WHERE transactions_id = %s
    ''',(return_date,transaction_id))

    cursor.execute('UPDATE Books SET availability = %s WHERE book_id = %S',(True,book_id))
    conn.commit()


def list_available_books():
    cursor.execute('SELECT * FROM Books WHERE availability = TRUE')
    books = cursor.fetchall()
    for book in books:
        print(book)




create_tables()
add_book('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 1925)
borrow_book(1, 1)  
list_available_books() 


conn.close()