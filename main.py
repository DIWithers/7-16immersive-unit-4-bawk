from flask import Flask, render_template, redirect, request, session
from flaskext.mysql import MySQL
import bcrypt


app = Flask(__name__)
mysql = MySQL()
#Add to the app (flask object) some config data for our connection
#config is a dictionary
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'BAWK'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
#use the mysql object's method "init_app" and pass it the flask object
mysql.init_app(app)

#Make one re-usable connection
conn = mysql.connect()
#set up cursor object which sql can use and run queries
cursor = conn.cursor()

#secret key needed for sessions to work #salt for the session #gets encrypted
app.secret_key = "drhshsdgeajhsrjgewaetjtdyjsrhwasdgfasdg42224352352"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login")
def login():
	return render_template("login.html")	

@app.route("/register")
def register():
	if request.args.get("username"):
		return render_template("register.html",
			message = "That username is already taken.")
	else:
		return render_template("register.html")	

@app.route("/register_submit", methods=['POST'])
def register_submit():
	print request.form
	# Is the username taken? SELECT statement
	check_username_query = "SELECT * FROM user WHERE username = '%s'" % request.form['username']
	cursor.execute(check_username_query)
	check_username_result = cursor.fetchone()
	if check_username_result is None: #no match, need to insert

		full_name = request.form['full_name']
		username = request.form['username']
		password = request.form['password'].encode("utf-8")
		email = request.form['email']
		# avatar
		hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
		print hashed_password
		insert_username_query = "INSERT INTO user VALUES (DEFAULT, %s, %s, %s, %s, NULL)"
		cursor.execute(insert_username_query, (full_name, username, hashed_password, email))
		conn.commit()
		return redirect("/")
	else:
		return redirect("/register?username=taken")

	print check_username_result
	return "Done"
	# If taken, route back to register page with msg
	
@app.route("/login_submit", methods = ["POST"])
def login_submit():
	password = request.form['password'].encode("utf-8")

	check_user_query = "SELECT * FROM user WHERE username = '%s'" % request.form['username']
	cursor.execute(check_user_query)
	check_user_result = cursor.fetchone()
	print check_user_result

	if check_user_result is None:
		return render_template("login.html", message = "Wrong username. Please check the username and try again or REGISTER." )

	hashed_password_from_mysql_query = check_user_result[3]
	hashed_password_from_mysql_encoded = hashed_password_from_mysql_query.encode("utf-8")

	hashed_password_from_login = bcrypt.hashpw(password, bcrypt.gensalt())
	# return hashed_password_from_mysql
	# to check a hash against english...
	# print hashed_password_from_login

	if bcrypt.checkpw(password, hashed_password_from_mysql_encoded):
		print "Login SUCCESS!!!!"
		session["username"] = request.form["username"]
		#welcome the user?
		return render_template("index.html", welcome_msg = "Welcome,  " + check_user_result[1])
		
	else:
		return render_template("login.html", message = "Wrong password. Please try again." )
		

@app.route("/logout")
def logout():
	session.clear() #ends session
	return render_template("index.html", message = "Logged out successfully." )

if __name__ == "__main__":
	app.run(debug=True)

