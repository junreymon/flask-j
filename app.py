# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['logged'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'REGISTRO EXITOSO A LA BASE DE DATOS'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Datos inorrectos'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('logged', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'ESTA CUENTA YA EXISTE'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'EMAIL INCORRECTO !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'CARCATRES INVALIDOS'
		elif not username or not password or not email:
			msg = 'DIJITE INFORMACION EN EL CAMPO REQUERIDO'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'SE HA REGISTRADO CORRECTAMENTE'
	elif request.method == 'POST':
		msg = 'DIJITE INFORMACION EN EL CAMPO REQUERIDO'
	return render_template('register.html', msg = msg)
