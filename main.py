from flask import Flask, render_template, redirect, request, session, jsonify
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
	retrieve_post_query = "SELECT buzzes.id, post_content, current_vote, timestamp, username, avatar FROM buzzes INNER JOIN user ON user.id = buzzes.uid ORDER BY timestamp DESC limit 50"
	cursor.execute(retrieve_post_query)
	buzzes = cursor.fetchall()

	return render_template("index.html", buzzes = buzzes, avatar = session["avatar"], username = session["username"])



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
		insert_username_query = "INSERT INTO user VALUES (DEFAULT, %s, %s, %s, %s, DEFAULT)"
		cursor.execute(insert_username_query, (full_name, username, hashed_password, email))
		conn.commit()

		# shortcut so user doesn't have to log in right after registering
		session["username"] = request.form["username"]
		session["full_name"] = request.form["full_name"]
		session["avatar"] = "bee_neutral.png"
		retrieve_post_query = "SELECT buzzes.id, post_content, current_vote, timestamp, username, avatar FROM buzzes INNER JOIN user ON user.id = buzzes.uid ORDER BY timestamp DESC limit 50"
		cursor.execute(retrieve_post_query)
		buzzes = cursor.fetchall()
		#Need this if the user wants to post right after registration
		check_user_query = "SELECT * FROM user WHERE username = '%s'" % session["username"]
		cursor.execute(check_user_query)
		check_user_result = cursor.fetchone()
		session["id"] = check_user_result[0]

		#welcome the user?
		return render_template("index.html", welcome_msg = "Welcome, " + session["full_name"], messagePos = "Registration successful.", buzzes = buzzes, avatar = session["avatar"])
	else:
		return redirect("/register?username=taken")

	print check_username_result
	return "Done"
	# If taken, route back to register page with msg
	
@app.route("/login_submit", methods = ["POST"])
def login_submit():
	retrieve_post_query = "SELECT buzzes.id, post_content, current_vote, timestamp, username, avatar FROM buzzes INNER JOIN user ON user.id = buzzes.uid ORDER BY timestamp DESC limit 50"
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

	if bcrypt.checkpw(password, hashed_password_from_mysql_encoded):
		print "Login SUCCESS!!!!"
		session["username"] = request.form["username"]
		session["id"] = check_user_result[0]
		session["full_name"] = check_user_result[1]
		session["avatar"] = check_user_result[5]
		print check_user_result[5]
		#welcome the user

		return render_template("index.html", welcome_msg = "Welcome,  " + session["full_name"], buzzes = buzzes, avatar = session["avatar"], username = session["username"] )
		
	else:
		return render_template("login.html", message = "Wrong password. Please try again." )
@app.route("/post_submit", methods=["POST"])
def post_submit():
	#first post
	post_content = request.form["post_content"]
	insert_post_query = "INSERT INTO buzzes VALUES (DEFAULT, %s, %s, DEFAULT, DEFAULT)"
	cursor.execute(insert_post_query, (post_content, session["id"]))
	conn.commit()

	#then a query
	retrieve_post_query = "SELECT buzzes.id, post_content, current_vote, timestamp, username, avatar FROM buzzes INNER JOIN user ON user.id = buzzes.uid ORDER BY timestamp DESC limit 50"
	cursor.execute(retrieve_post_query)
	buzzes = cursor.fetchall()
	avatar = session["avatar"]
	return render_template("index.html", welcome_msg = "Welcome,  " + session["full_name"], buzzes = buzzes, avatar = session["avatar"], username = session["username"] )

@app.route("/upload_avatar", methods = ["POST"])	
def upload_avatar():
	username = session["username"]
	image = request.files["image_link"]

	if image:
	#upload and update
		image.save("static/images/avatars/" + image.filename)
		image_path = image.filename
		query = "UPDATE user SET avatar = %s WHERE username = %s"
		cursor.execute(query, (image_path, username))
		session['avatar'] = image_path #new avatar set in session
		#refresh query for buzzes
		retrieve_post_query = "SELECT buzzes.id, post_content, current_vote, timestamp, username, avatar FROM buzzes INNER JOIN user ON user.id = buzzes.uid ORDER BY timestamp DESC limit 50"
		cursor.execute(retrieve_post_query)
		buzzes = cursor.fetchall()
		avatar = session["avatar"]

		return render_template("index.html", welcome_msg = "Welcome,  " + session["full_name"], buzzes = buzzes, avatar = avatar)
	else:
		retrieve_post_query = "SELECT buzzes.id, post_content, current_vote, timestamp, username, avatar FROM buzzes INNER JOIN user ON user.id = buzzes.uid ORDER BY timestamp DESC limit 50"
		cursor.execute(retrieve_post_query)
		buzzes = cursor.fetchall()
		avatar = session["avatar"]
		return render_template("index.html", welcome_msg = "Welcome,  " + session["full_name"], buzzes = buzzes, avatar = avatar, message = "Please provide an image to upload.")

################# EDIT AVATAR ##################
@app.route("/edit_avatar", methods = ["POST"])
def edit_avatar():
	#edit and update
	print "EEEEEDDDDDDIIIIIIITTTTT"
	session["avatar"] = request.form["avatar"]
	avatar = session["avatar"]
	username = session['username']
	if avatar:
		query = "UPDATE user SET avatar = %s WHERE username = %s"
		cursor.execute(query, (avatar, username))
		retrieve_post_query = "SELECT buzzes.id, post_content, current_vote, timestamp, username, avatar FROM buzzes INNER JOIN user ON user.id = buzzes.uid limit 50"
		cursor.execute(retrieve_post_query)
		buzzes = cursor.fetchall()
		avatar = session["avatar"]
		return render_template("index.html", welcome_msg = "Welcome,  " + session["full_name"], buzzes = buzzes, avatar = avatar)

@app.route("/edit_complete", methods = ["POST"]) #because of async
def edit_complete():
	retrieve_post_query = "SELECT buzzes.id, post_content, current_vote, timestamp, username, avatar FROM buzzes INNER JOIN user ON user.id = buzzes.uid ORDER BY timestamp DESC limit 50"
	cursor.execute(retrieve_post_query)
	buzzes = cursor.fetchall()
	avatar = session["avatar"]
	return render_template("index.html", welcome_msg = "Welcome,  " + session["full_name"], buzzes = buzzes, avatar = avatar)

@app.route("/process_vote", methods= ["POST"])
def process_vote():
	#has the user voted on this particular item?
	pid = request.form["pid"]
	vote_type = request.form["vote_type"]
	uid = session["id"]
	username = session["username"]
	avatar = session["avatar"]
	print pid
	print uid
	print vote_type
	check_user_votes_query = "SELECT * FROM votes INNER JOIN user ON user.id = votes.uid WHERE user.username = %s AND votes.pid = %s" 
	print check_user_votes_query
	cursor.execute(check_user_votes_query, (username, pid))
	check_user_votes_result = cursor.fetchone()

	print check_user_votes_result
	# It's possible we get none back bc the user hasn't voted on this post...
	if check_user_votes_result is None: #insert needed
		print "No votes"
		insert_user_vote_query = "INSERT INTO votes VALUES (DEFAULT, %s, %s, %s)"
		cursor.execute(insert_user_vote_query, (pid, uid, vote_type))
		conn.commit() #success!
		vote_count_sum = "SELECT SUM(vote_type) FROM votes WHERE pid ='%s'" % pid #running total
		cursor.execute(vote_count_sum)
		vote_total = cursor.fetchone()
		
		return jsonify({"message": "voteCounted", "vote_total": int(vote_total[0])})
	
	else: #revamp
		check_user_vote_direction_query = "SELECT * FROM votes INNER JOIN user ON user.id = votes.uid WHERE user.username = '%s' AND votes.pid = '%s' AND votes.vote_type = %s" % (session['username'], pid, vote_type)
		cursor.execute(check_user_vote_direction_query)
		check_user_vote_direction_result = cursor.fetchone()
		if check_user_vote_direction_result is None:
			# User has voted, but not this direction. Update
			update_user_vote_query = "UPDATE votes SET vote_type = %s WHERE uid = '%s' AND pid = '%s'" % (vote_type, session['id'], pid)
			cursor.execute(update_user_vote_query)
			conn.commit()
			vote_count_sum = "SELECT SUM(vote_type) FROM votes WHERE pid ='%s'" % pid #running total
			cursor.execute(vote_count_sum)
			vote_total = cursor.fetchone()
			
			return jsonify({'message': "voteChanged", 'vote_total': int(vote_total[0])})
		else:
			return jsonify({'message': "alreadyVoted"})
		
@app.route("/follow")
def follow():
	get_other_users_query = "SELECT * FROM user WHERE id != '%s'" % session["id"]
	cursor.execute(get_other_users_query)

	get_all_followed = "SELECT follow.uid_of_followed, user.username, user.avatar FROM follow LEFT JOIN user ON user.id = follow.uid_of_followed WHERE follow.uid_of_follower = '%s'" % session["id"]
	cursor.execute(get_all_followed)
	get_all_followed_result = cursor.fetchall()

	get_all_not_followed = "SELECT id, username, avatar from user WHERE id NOT IN (SELECT uid_of_followed FROM follow WHERE uid_of_follower = '%s') AND id != '%s'" % (session['id'], session['id'])
	cursor.execute(get_all_not_followed)
	get_all_not_followed_result = cursor.fetchall()

	# return render_template('follow.html')
	return render_template('follow.html',
		followed_list = get_all_followed_result,
		not_followed_list = get_all_not_followed_result)


@app.route("/follow_user")
def follow_user():
	user_id_to_follow = request.args.get('user_id')
	follow_query = "INSERT INTO follow (uid_of_followed, uid_of_follower) VALUES ('%s', '%s')" % (user_id_to_follow, session['id'])
	cursor.execute(follow_query)
	conn.commit()
	return redirect("/follow")

@app.route("/unfollow_user")
def unfollow_user():
	user_id_to_unfollow = request.args.get('user_id')
	unfollow_query = "DELETE FROM follow WHERE uid_of_followed = '%s' AND uid_of_follower = '%s'" % (user_id_to_unfollow, session['id'])
	cursor.execute(unfollow_query)
	conn.commit()
	return redirect("/follow")

@app.route("/logout")
def logout():
	session.clear() #ends session
	buzzes = ""
	return render_template("index.html", message = "Logged out successfully." )

if __name__ == "__main__":
	app.run(debug=True)

