import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="SQLroot",
  database="cookbook_database"
)
cursor = mydb.cursor()

def insert_post():
  sql = "INSERT INTO posts (post_creator, post_title, post_path) VALUES (%s, %s, %s)"
  val = ("Connor91", "Grandma's Apple Pie", "C:\\Users\\Connor\\Documents\\Cookbook\\Posts\\Connor91\\100.json")
  cursor.execute(sql, val)
  mydb.commit()

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

def generate_post_id():
  # get the post with the highest id
  sql = "SELECT postid FROM posts ORDER BY postid DESC"
  cursor.execute(sql)
  myresult = cursor.fetchone()
  return (myresult[0] + 1)

def add_user(use_email):
  file_preamble = "C:\\Users\\Connor\\Documents\\Cookbook\\Users\\"
  settings_path = file_preamble + "Connor91" + "\\settings.json"
  log_file_path = file_preamble + "Connor91" + "\\logfile.json"
  if use_email != True:
    sql = "INSERT INTO users (username, pass, displayname, settings, `logfile`) VALUES (%s, %s, %s, %s, %s)"
    val = ("Connor91", "password123", "Connor91", settings_path, log_file_path)
  else:
    email = "con@gmail.com"
    sql = "INSERT INTO users (username, pass, email, displayname, settings, `logfile`) VALUES (%s, %s, %s, %s, %s, %s)"
    val = ("Connor91", "password123", email, "Connor91", settings_path, log_file_path)
  cursor.execute(sql, val)
  mydb.commit()

# print("Connor91 exists: " + str(check_if_username_exists("Connor91")))
# print("Connor92 exists: " + str(check_if_username_exists("Connor92")) +"\n")
# # print(getPassword("Connor91"))
# getPassword("Connor91")
# # insert_post()
# print("Next post id: " + str(generate_post_id()))
add_user(True)