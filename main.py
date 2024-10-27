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
cursor = mydb.cursor(buffered=True)

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
        sql_cmnd = "INSERT INTO users (username, pass, displayname, settings, `logfile`) VALUES (%s, %s, %s, %s, %s)"
        val = (username, password, username, settings_path, log_file_path)
      else:
        email = request.form["email"]
        sql_cmnd = "INSERT INTO users (username, pass, email, displayname, settings, `logfile`) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (username, password, email, username, settings_path, log_file_path)
      cursor.execute(sql_cmnd, val)
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
    sql_cmnd = "INSERT INTO posts (post_creator, post_title, post_path) VALUES (%s, %s, %s)"
    val = (username, post_dict["title"], file_path)
    cursor.execute(sql_cmnd, val)
    mydb.commit()
    # return home
    return redirect(url_for("home"))
  else:
    return render_template("post-creation.html")

@app.route("/loadPostsPg<number>")
def load_3_posts(number):
  number = int(number)
  post_dict = {0:None, 1:None, 2:None}
  sql_cmnd = "SELECT post_path FROM posts ORDER BY postid DESC"
  cursor.execute(sql_cmnd)
  myresult = cursor.fetchall()
  for i in range(number, 3):
    file_path = myresult[i][0]
    # load post as json from the post's file location
    with open(file_path, mode="r", encoding="utf-8") as read_file:
      post_dict[i] = json.load(read_file)

  post_json = json.dumps(post_dict)
  return post_json

@app.route("/viewProfilePage")
def view_profile_page():
  return render_template("viewProfilePage.html")

@app.route("/ProfileSettings")
def profile_settings():
  return render_template("ProfileSettings.html")

@app.route("/BookmarkPage")
def bookmark_page():
  return render_template("BookmarkPage.html")

# helper functions
def getPassword(username):
  # communicate with database to check if the username matches the password
  sql_cmnd = f"SELECT pass FROM users WHERE username ='{username}'"
  cursor.execute(sql_cmnd)
  result = cursor.fetchone()
  return result[0]

def check_if_username_exists(username):
  # communicate with database to check if the username exists
  sql_cmnd = f"SELECT username FROM users"
  cursor.execute(sql_cmnd)
  result = cursor.fetchall()
  for name in result:
    if name[0] == username:
      return True
  return False

def post_to_dict(post, username):
  post_dict = {"username": username}
  post_dict["title"] = post["title"]
  post_dict["description"] = post["description"]
  # the ingredients get posted as a string like this: "ingr1, ingr2, etc"
  # so they must be split into a list of strings before storing as json
  post_dict["ingredients"] = post["ingredientList"].split(", ")
  post_dict["instructions"] = post["instructions"]
  # the tags also get posted as a string like this: "#tag1, #tag2, etc"
  # so they must also be split into a list of strings before storing
  post_dict["tags"] = post["tagField"].split(", ")
  return post_dict

def generate_post_id():
  # get the post with the highest id
  sql_cmnd = "SELECT postid FROM posts ORDER BY postid DESC"
  cursor.execute(sql_cmnd)
  myresult = cursor.fetchone()
  # handle if there are no posts in the database
  if(myresult == None):
    return(100)
  else:
    return (myresult[0] + 1)

if __name__ == "__main__":
  app.run(debug=True)