from dotenv import load_dotenv
import os


load_dotenv()
db_user = os.getenv("db_user")
db_pw = os.getenv("db_pw")


dbconfig = {
  "database": "wehelp2",
  "user": db_user,
  "password": db_pw,
  "auth_plugin":'mysql_native_password'
}

