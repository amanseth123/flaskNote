
'''
app=Flask(__name__)
@app.route('/')
def index():
    return "hello Aman"
@app.route('/<name>')
def printName(name):
    return 'Hi, {}'.format(name)
if __name__=='__main__':
    app.run(debug=True)   
'''
#                           LOGIN Features

# Store this code in 'app.py' file 

from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 
import mysql.connector
app = Flask(__name__) 
#app.secret_key = 'your secret key'
import secrets
secret = secrets.token_urlsafe(32)
app.secret_key = secret
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aman123'
app.config['MYSQL_DB'] = 'geeklogin'
mysql = MySQL(app) 
@app.route('/') 
@app.route('/login', methods =['GET', 'POST']) 
def login():
    msg = ''
    if request.method == 'POST' and 'authorname' in request.form and 'password' in request.form: 
	    username = request.form['authorname'] 
	    password = request.form['password'] 
	    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
	    cursor.execute('SELECT * FROM accounts WHERE authorname = % s AND password = % s', (username, password, )) 
	    account = cursor.fetchone() 
	    if account: 
		    session['loggedin'] = True
		    session['id'] = account['id'] 
		    session['authorname'] = account['authorname'] 
		    msg = 'Logged in successfully !'
		    return render_template('index.html', msg = msg) 
	    else: 
		    msg = '123 Incorrect username / password !'
    return render_template('login.html', msg = msg) 

@app.route('/logout') 
def logout(): 
	session.pop('loggedin', None) 
	session.pop('id', None) 
	session.pop('authorname', None) 
	return redirect(url_for('login')) 

@app.route('/register', methods =['GET', 'POST']) 
def register():
    msg = ''
    msg+= str(request.method) + str(request.form)
    if request.method == 'POST' and 'authorname' in request.form and 'password' in request.form and 'email' in request.form :
        msg+="play"
        username = request.form['authorname']
        password = request.form['password']
        email = request.form['email']
        title="connectionDB"
        language="English"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE authorname = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form 3!'
        else:
            msg+="hello" 
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s,% s,%s)', (username, password,title, language, email, )) 
            mysql.connection.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg += 'Please fill out the form 2!'
    return render_template('register.html', msg = msg) 
#                           LOGIN Features End

def db_connection():
    #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor=mysql.connector.connect(user='root', database='geeklogin')
    return cursor

@app.route('/books',methods=['Get','POST'])
def books():
    #conn=db_connection()
    cursor = db_connection()
    print("Request method",str(request.method))
    if request.method=='GET':
        result = cursor.execute("SELECT * FROM accounts")
        print("Result ",result)
        #result=cursor.fetchall()
        books=[
            dict(id=row[0],author=row[1],language=row[4],title=row[3])
            for row in result
        ]
        if books is not None:
            return jsonify(books)

    if request.method=='POST':
        new_author = request.form['authorname']
        new_lang =request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO accounts (authorname,language,title) VALUES (?,?,?)"""
        cursor.execute(sql,(new_author,new_lang,new_title))
        #c.commit()
        return f"Book with the id:{cursor.lastrowid} created succcessfully",201
     
@app.route('/books/<int:id>',methods=['GET','PUT','DELETE'])
def single_book(id):
    #conn=db_connection()
    #cursor = conn.cursor()
    cursor=db_connection()
    book=None
    if request.method=='GET':
        result = cursor.execute("SELECT * FROM accounts WHERE id=?",(id,))
        #rows=cursor.fetchone()
        rows=result.fetchall()
        for r in rows:
            book=r
        if book is not None:
            return jsonify(book),200
        else:
            return "Something went wrong",404
    if request.method=='PUT':
        sql=""" UPDATE accounts SET title=?,
        authorname=?,
        language=?
        WHERE id=? """
        author= request.form['authorname']
        language = request.form['language']
        title = request.form['title']
        updated_book={
            'id':id,
            'authorname':book['authorname'],
            'language':book['language'],
            'title':book['title']
        }
        #conn.execute(sql,(author,language,title,id))
        cursor.execute(sql,(author,language,title,id))
        #conn.commit()
        return jsonify(updated_book)
    if request.method == 'DELETE':
        sql="""DELETE FROM accounts WHERE id=?"""
        cursor.execute(sql,(id,))
        #conn.commit()
        return "The book with id: {} has been deleted".format(id),200

if __name__ =='__main__':
    app.run(debug=True)



