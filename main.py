from flask import Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
import json
import os
from datetime import timedelta

HOST_NAME = os.getlogin()
PARENT_DIR = f"C:\\Users\\{HOST_NAME}\\Documents\\Cookbook_Files\\"

# connect to database
mydb = mysql.connector.connect(
  user="root",
  password="SQLroot",
  host="localhost",
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
      generate_new_user_folder(username)
      settings_path = PARENT_DIR + "Users\\" + username + "\\settings.json"
      log_file_path = PARENT_DIR + "Users\\" + username + "\\logfile.json"
      bookmarks_path = PARENT_DIR + "Users\\" + username + "\\bookmarks.json"
      if request.form["email"] == None or request.form["email"] == '':
        sql_cmnd = "INSERT INTO users (username, pass, settings, `logfile`, bookmarks) VALUES (%s, %s, %s, %s, %s)"
        val = (username, password, settings_path, log_file_path, bookmarks_path)
      else:
        email = request.form["email"]
        print(email)
        sql_cmnd = "INSERT INTO users (username, pass, email, settings, `logfile`, bookmarks) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (username, password, email, settings_path, log_file_path, bookmarks_path)
      cursor.execute(sql_cmnd, val)
      mydb.commit()
      # add user to the session
      session["user"] = username
      return redirect(url_for("home"))
  else:
    return render_template("newAccountPage.html")

@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("login"))

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
    post_id = generate_post_id()
    file_path = PARENT_DIR + "Posts\\" + str(post_id) + ".json"
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
  start = number*3
  end = (number*3)+3
  dict_index = 0
  for i in range(start, end):
    file_path = myresult[i][0]
    # load post as json from the post's file location
    with open(file_path, mode="r", encoding="utf-8") as read_file:
      post_dict[dict_index] = json.load(read_file)
    dict_index+=1

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

@app.route("/grabBookmarks")
def grab_bookmarks():
  username = session["user"]
  # TODO: replace this with SQL request
  path = PARENT_DIR + "Users\\" + username + "\\bookmarks.json"
  # if the user has never bookmarked anything
  if os.path.isfile(path) == False:
    empty_json = {
      "isEmpty" : True,
      "0": None
    }
    return json.dumps(empty_json)
  else:
    # open the list of the user's bookmarks
    with open(path, mode="r", encoding="utf-8") as read_bookmark_list:
      post_id_json = json.load(read_bookmark_list)
    post_ids = post_id_json["bookmarks"]
    # if the user has something bookmarked
    if post_ids["isEmpty"] == False:
      # for each post id in the list, grab the path to that post, load it, and insertit into the dictonary that we're going to return
      posts_dict = {"isEmpty" : False}
      num = 0
      for id in post_ids:
        # TODO: replace this with function call
        sql_cmnd = f"SELECT post_path FROM posts WHERE postid = {id}"
        cursor.execute(sql_cmnd)
        post_path = cursor.fetchone()
        # load post as json from the post's file location
        with open(post_path[0], mode="r", encoding="utf-8") as read_post_json:
          posts_dict[num] = json.load(read_post_json)
        num += 1
      return json.dumps(posts_dict)
    else:
      # if the user doesn't have anything bookmarked
      empty_json = {  
        "isEmpty" : True,
        "0": None
      }
      return json.dumps(empty_json)


@app.route("/bookmarkPost<id>")
def save_bookmark(id):
  username = session["user"]
  # if this is the first post the user is bookmarking, then create a file to store their bookmarks in
  # TODO: replace this with SQL query
  path = PARENT_DIR + "Users\\" + username + "\\bookmarks.json"
  if os.path.isfile(path) == False:
    empty_json = {"bookmarks" : []}
    with open(path, mode="w", encoding="utf-8") as write_file:
      json.dump(empty_json, write_file)

  # load the user's bookmark file
  bookmark_dict = None
  with open(path, mode="r", encoding="utf-8") as read_file:
    bookmark_dict = json.load(read_file)

  # add the post to the bookmarks
  bookmark_dict["bookmarks"].append(id)

  # save the json file
  with open(path, mode="w", encoding="utf-8") as write_file:
    json.dump(bookmark_dict, write_file)
  return "Post bookmarked!"

@app.route("/unbookmarkPost<id>")
def del_bookmark(id):
  username = session["user"]
  # TODO: replace this with SQL query
  path = PARENT_DIR + "Users\\" + username + "\\bookmarks.json"
  # load the user's bookmark file
  bookmark_dict = None
  with open(path, mode="r", encoding="utf-8") as read_file:
    bookmark_dict = json.load(read_file)

  # remove the post from the bookmarks
  bookmark_dict["bookmarks"].remove(id)

  # save the json file
  with open(path, mode="w", encoding="utf-8") as write_file:
    json.dump(bookmark_dict, write_file)
  return "Post unbookmarked!"

@app.route("/viewFollowingFollowersPage")
def followers_page():
  return render_template("viewFollowingFollowersPage.html")

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

def generate_new_folders():
  # thanks to https://www.geeksforgeeks.org/create-a-directory-in-python/ for help with this function
  try:
    # create new posts path
    posts_path = PARENT_DIR + "Posts"
    os.makedirs(posts_path)
    print(f"Directory '{posts_path}' created successfully.")
  except FileExistsError:
    print(f"Directory '{posts_path}' already exists.")
  except Exception as e:
    print(f"An error occurred: {e}")
  try:
    # create new users path
    users_path = PARENT_DIR + "Users"
    os.mkdir(users_path)
    print(f"Directory '{users_path}' created successfully.")
  except FileExistsError:
    print(f"Directory '{users_path}' already exists.")
  except Exception as e:
    print(f"An error occurred: {e}")

def generate_new_user_folder(username):
  # thanks to https://www.geeksforgeeks.org/create-a-directory-in-python/ for help with this function
  try:
    # create new posts path
    new_user_path = PARENT_DIR + "User\\" + username
    os.mkdir(new_user_path)
    print(f"Directory '{new_user_path}' created successfully.")
  except FileExistsError:
    print(f"Directory '{new_user_path}' already exists.")
  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == "__main__":
  generate_new_folders()
  app.run(debug=True)