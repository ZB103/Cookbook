from flask import Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
import json
from datetime import timedelta

# connect to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="SQLroot",
  database="cookbook_database"
)
cursor = mydb.cursor()

# flask stuff
app = Flask(__name__)
app.secret_key = "BookCook" # make this more complicated
app.permanent_session_lifetime = timedelta(hours=2)

@app.route("/login", methods=["POST", "GET"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    # if username doesn't exist
    if check_if_username_exists(username) == False:
      flash(f"This account does not exist.", "info")
      return render_template("signinPage.html")
    # if the user's password is the same as the password that was inputted
    elif getPassword(username) == password:
      session["user"] = username
      return redirect(url_for("home"))
    else:
      flash("Your username or password is incorrect. Please try again", "info")
      return render_template("signinPage.html")
  else:
    return render_template("signinPage.html")

@app.route("/newAccount", methods=["POST","GET"])
def new_account():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password1"]
    # check if username is taken
    if check_if_username_exists(username):
      flash(f"{username} is taken, please choose something else", "info")
      return redirect(url_for("new_account"))
    # make sure the passwords match
    elif password != request.form["password2"]:
      flash(f"Your passwords do not match, please try again", "info")
      return redirect(url_for("new_account"))
    else:
      # add user to database
      file_preamble = "C:\\Users\\Connor\\Documents\\Cookbook\\Users\\"
      settings_path = file_preamble + username + "\\settings.json"
      log_file_path = file_preamble + username + "\\logfile.json"
      if request.form["email"] == None:
        sql = "INSERT INTO users (username, pass, displayname, settings, `logfile`) VALUES (%s, %s, %s, %s, %s)"
        val = (username, password, username, settings_path, log_file_path)
      else:
        email = request.form["email"]
        sql = "INSERT INTO users (username, pass, email, displayname, settings, `logfile`) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (username, password, email, username, settings_path, log_file_path)
      cursor.execute(sql, val)
      mydb.commit()
      # add user to the session
      session["user"] = username
      return redirect(url_for("home"))
  else:
    return render_template("newAccountPage.html")

@app.route("/")
@app.route("/home")
def home():
  if "user" in session:
    user = session["user"]
    return render_template("homePage.html")
  else:
    return redirect(url_for("login"))

@app.route("/createPost", methods=["POST","GET"])
def create_post():
  if request.method == "POST":
    pass
    username = session["user"]
    # turn the form into a dictionary
    post_dict = post_to_dict(request.form, username)
    # generate new file location
    file_preamble = "C:\\Users\\Connor\\Documents\\Cookbook\\Posts\\"
    post_id = generate_post_id()
    file_path = file_preamble + username + "\\" + str(post_id) + ".json"
    # add post id to post dictionary
    post_dict["id"] = post_id
    # save post as json at that file location
    with open(file_path, mode="w", encoding="utf-8") as write_file:
      json.dump(post_dict, write_file)
    # insert post to database
    sql = "INSERT INTO posts (post_creator, post_title, post_path) VALUES (%s, %s, %s)"
    val = (username, post_dict["title"], file_path)
    cursor.execute(sql, val)
    mydb.commit()
    # return home
    return redirect(url_for("home"))
  else:
    return render_template("post-creation.html")




def getPassword(username):
  # communicate with database to check if the username matches the password
  command = f"SELECT pass FROM users WHERE username ='{username}'"
  cursor.execute(command)
  result = cursor.fetchone()
  return result[0]

def check_if_username_exists(username):
  # communicate with database to check if the username exists
  command = f"SELECT username FROM users"
  cursor.execute(command)
  result = cursor.fetchall()
  for name in result:
    if name[0] == username:
      return True
  return False

def post_to_dict(post, username):
  post_dict = {"username": username}
  post_dict["title"] = post["title"]
  post_dict["description"] = post["description"]
  post_dict["ingredients"] = post["ingredients"]
  post_dict["instructions"] = post["instructions"]
  post_dict["tags"] = post["tagField"]
  return post_dict

def generate_post_id():
  # get the post with the highest id
  sql = "SELECT postid FROM posts ORDER BY postid DESC"
  cursor.execute(sql)
  myresult = cursor.fetchone()
  return (myresult[0] + 1)


# @app.route("/user")
# def user():
#   if "user" in session:
#     user = session["user"]
#     return f"<h1>{user}</h1>"
#   else:
#     return redirect(url_for("login"))


# @app.route("/logout")
# def logout():
#   if "user" in session:
#     user = session["user"]
#     flash(f"{user} has been sucessfully logged out", "info")
#   session.pop("user", None)
#   # flash("You have been sucessfully logged out", "info")
#   return redirect(url_for("login"))

# @app.route("/admin")
# def admin():
#   return redirect(url_for("user", name="admin!"))

if __name__ == "__main__":
  app.run(debug=True)