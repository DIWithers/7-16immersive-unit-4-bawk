from flask import Flask, render_template, redirect, request, session
from flaskext.mysql import MySQL
import bcrypt


app = Flask(__name__)
mysql = MySQL()
#Add to the app (flask object) some config data for our connection
#config is a dictionary
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'buzz'
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
	retrieve_post_query = "SELECT * FROM buzzes limit 25"
	cursor.execute(retrieve_post_query)
	buzzes = cursor.fetchall()

	return render_template("index.html", buzzes = buzzes)



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
	cursor.execute(check_username_query) #id, full_name, username, password, email, avatar
	check_username_result = cursor.fetchone()
	if check_username_result is None: #no match, need to insert

		full_name = request.form['full_name']
		username = request.form['username']
		password = request.form['password'].encode("utf-8")
		email = request.form['email']
		# avatar
		hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
		# print hashed_password
		insert_username_query = "INSERT INTO user VALUES (DEFAULT, %s, %s, %s, %s, NULL)"
		cursor.execute(insert_username_query, (full_name, username, hashed_password, email))
		conn.commit()
		# shortcut so user doesn't have to log in right after registering
		session["username"] = request.form["username"]
		session["id"] = check_username_result[0]
		session["full_name"] = check_username_result[1]
		session["avatar"] = check_username_result[5]
		#welcome the user?
		return render_template("index.html", welcome_msg = "Welcome, " + session["full_name"])
	else:
		return redirect("/register?username=taken")

	print check_username_result
	return "Done"
	# If taken, route back to register page with msg


	####--------to-do, upload photo
		# image = request.files["avatar"]
		# image.save("static/images/avatars" + image.filename)
		# image_path = image.filename
		# query = "INSERT INTO page_content VALUES (DEFAULT, 'home', %s, %s, 1, 1, 'left_block', NULL, %s)"
		# cursor.execute(query, (avatar))
		# conn.commit()
	###----------
	
@app.route("/login_submit", methods = ["POST"])
def login_submit():
	retrieve_post_query = "SELECT * FROM buzzes limit 25"
	cursor.execute(retrieve_post_query)
	buzzes = cursor.fetchall()

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
		session["id"] = check_user_result[0]
		session["full_name"] = check_user_result[1]
		session["avatar"] = check_user_result[5]
		#welcome the user?

		return render_template("index.html", welcome_msg = "Welcome,  " + session["full_name"], buzzes = buzzes, avatar = session["avatar"] )
		# return redirect("/")
		
	else:
		return render_template("login.html", message = "Wrong password. Please try again." )
@app.route("/post_submit", methods=["POST"])
def post_submit():
	#first post
	post_content = request.form["post_content"]
	insert_post_query = "INSERT INTO buzzes VALUES (DEFAULT, %s, %s, DEFAULT)"
	cursor.execute(insert_post_query, (post_content, session["id"]))
	conn.commit()

	#then a query
	retrieve_post_query = "SELECT * FROM buzzes limit 25"
	cursor.execute(retrieve_post_query)
	buzzes = cursor.fetchall()

	return render_template("index.html", welcome_msg = "Welcome,  " + session["full_name"], buzzes = buzzes, avatar = session["avatar"])	
@app.route("/edit_avatar", methods=["POST"])
def edit_avatar():
	image = request.files["avatar"]
	image.save("static/images/avatars" + image.filename)
	image_path = image.filename

	query = "UPDATE user SET avatar = %s WHERE username = '%s'" % session["username"]
	cursor.execute(query, (image))

@app.route("/logout")
def logout():
	session.clear() #ends session
	return render_template("index.html", message = "Logged out successfully." )


@app.route("/process_vote", methods= ["POST"])
def process_vote():
	#has the user voted on this particular item?
	pid = reuest.form["pid"]
	check_user_votes_query = "SELECT * FROM votes INNER JOIN user user.id = votes.uid WHERE user.username = '%s' AND votes.pid = '%s' " % session["id"], pid
	cursor.execute(check_user_result)
	check_user_votes_result = cursor.fetchone()
	# It's possible we get none back bc the user hasn't voted on this post...
	if check_user_votes_result is None: #insert needed
		insert_user_vote_query = "INSERT INTO votes (pid, uid, voteType) VALUES ('"+pid+"', '"+session['id']+"', '"+voteType+"')"
		cursor.execute(insert_user_vote_query)
		conn.commit()
	return jsonify(request.form["pid"])
if __name__ == "__main__":
	app.run(debug=True)

