from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
app.secret_key = 'Secret'
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

mysql = MySQLConnector('emailsdb')
@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html')
@app.route('/emails', methods = ['POST'])
def create():
	if len(request.form['email']) < 1:
		flash("email cannot be empty!")
		return redirect ('/')
	elif not EMAIL_REGEX.match(request.form['email']):
		flash('Invalid email address!')
		return redirect('/')
	else:
		emails = mysql.fetch("SELECT * FROM emails")
		query = "INSERT INTO emails (email, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(request.form['email'])
		print query
		mysql.run_mysql_query(query)
		flash('The email address you entered is a VALID email address! Thank You!')
		return render_template('email.html', emails=emails)
@app.route('/delete', methods = ['POST'])
def delete():
	query = "DELETE FROM emails WHERE email = '{}'".format(request.form['delete'])
	mysql.run_mysql_query(query)
	emails = mysql.fetch("SELECT * FROM emails")
	return render_template('email.html', emails=emails)


app.run(debug=True)