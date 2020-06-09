from flask import Flask, render_template, url_for, request, redirect
import sqlite3


conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS annotations (id INTEGER PRIMARY KEY AUTOINCREMENT, imgname TEXT, annotation TEXT)')
conn.close()


app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/do_register', methods=['POST'])
def do_register():
	username = request.form['username']
	password = request.form['password']
	
	conn = sqlite3.connect("database.db")
	cur = conn.cursor()
	cur.execute("INSERT INTO users VALUES (?,?)", (username, password))
	conn.commit()
	conn.close()

	return render_template('message.html', title='registration', message='Registration successful')


@app.route('/do_login', methods=['POST'])
def do_login():
	username = request.form['username']
	password = request.form['password']
	
	conn = sqlite3.connect("database.db")
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
	
	if len(cur.fetchall()) > 0:
		return redirect(url_for('images'))
	else:
		conn.close()
		return render_template('message.html', title='login', message='Login unsuccessful')


@app.route('/images')
def images():
	filenames = ['images/img_' + str(i) + '.png' for i in range(30)]
	return render_template('images.html', filenames=filenames)


@app.route('/annotate/<filename>')
def annotate(filename):
	return render_template('annotate.html', filename=filename)


@app.route('/do_annotate')
def do_annotate():
	imgname = request.args.get('imgname')
	annotation = request.args.get('annotation')
	
	conn = sqlite3.connect("database.db")
	cur = conn.cursor()
	cur.execute("INSERT INTO annotations (imgname, annotation) VALUES (?,?)", (imgname, annotation))
	conn.commit()
	conn.close()
	return render_template('message.html', title='annotation', message='Thank you for annotating')


app.run(debug=True)
