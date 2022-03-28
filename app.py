from flask import *
import jwt
import time
import mysql.connector
import mysql.connector.pooling

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False  # not to Sort the keys of JSON objects alphabetically

# mydb1 = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="vaapad666",
#     database="wehelp2",
#     auth_plugin='mysql_native_password'
# )

# mydb2 = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="vaapad666",
#     database="wehelp2",
#     auth_plugin='mysql_native_password'
# )

# connection pool
dbconfig = {
  "database": "wehelp2",
  "user": "root",
  "password": "vaapad666",
  "auth_plugin":'mysql_native_password'
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool", pool_size = 3, pool_reset_session=True, **dbconfig)

# session key
# app.secret_key = "wingardiumleviosawingardiumleviosa"

# jwt key
key = "wingardiumleviosawingardiumleviosa"



# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/api/attractions")
def api_attractions():
    cnx1 = cnxpool.get_connection()
    mycursor = cnx1.cursor()
    # mycursor = mydb1.cursor(buffered=True)
    page = request.args.get("page", default=0, type=int)
    keyword = request.args.get("keyword", default="", type=str)
    mycursor.execute("SELECT COUNT(*) FROM attractions WHERE name LIKE %s", (f'%{keyword}%',))
    (total,) = mycursor.fetchone()

    if total > 0:
        for i in range(0, total, 12):

            if page == i/12:
                mycursor.execute("SELECT id, name, category, description, address, transport, mrt, latitude, longitude FROM attractions WHERE name LIKE %s LIMIT %s, 12", (f'%{keyword}%', i))
                db_data = mycursor.fetchall()
                page_data = {
                    "nextPage": page+1 if page < (total//12) else None,
                    "data": []
                }
                for i in range(len(db_data)):
                    (id, name, category, description, address, transport, mrt, latitude, longitude) = db_data[i]
                    mycursor.execute(f"SELECT img_url FROM photos WHERE attraction_id ={id}")
                    images = []

                    for x in mycursor.fetchall():
                        img = x[0]
                        images.append(img)

                    attract_info = {
                        "id": id,
                        "name": name,
                        "category": category,
                        "description": description,
                        "address": address,
                        "transport": transport,
                        "mrt": mrt,
                        "latitude": latitude,
                        "longitude": longitude,
                        "images": images
                    }

                    page_data["data"].append(attract_info)

            elif page > (total // 12):
                page_data = {
                    "error": True,
                    "message": "伺服器內部錯誤，此頁無景點資料，請試試前頁"
                }

    else:
        page_data = {
                    "error": True,
                    "message": "查無此景點資料"
                }
    mycursor.close()
    cnx1.close()
    return jsonify(page_data)


@app.route("/api/attraction/<attractionId>")
def attract_id(attractionId):
    # mycursor = mydb1.cursor(buffered=True)
    cnx1 = cnxpool.get_connection()
    mycursor = cnx1.cursor()
    try:
        mycursor.execute("SELECT id, name, category, description, address, transport, mrt, latitude, longitude FROM attractions WHERE id = %s", (attractionId,))
        attract_data = mycursor.fetchone()

        if mycursor.rowcount == 1:
            (id, name, category, description, address, transport, mrt, latitude, longitude) = attract_data
            mycursor.execute("SELECT img_url FROM photos WHERE attraction_id =%s", (attractionId,))
            images = []

            for x in mycursor.fetchall():
                img = x[0]
                images.append(img)

            attract_info = {
                "data": {
                    "id": id,
                    "name": name,
                    "category": category,
                    "description": description,
                    "address": address,
                    "transport": transport,
                    "mrt": mrt,
                    "latitude": latitude,
                    "longitude": longitude,
                    "images": images
                }
            }

        else:
            attract_info = {
                "error": True,
                "message": "景點編號不正確"
            }

    except:
        attract_info = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
    mycursor.close()
    cnx1.close()
    return jsonify(attract_info)


@app.route("/api/user", methods=["GET", "POST", "PATCH", "DELETE"])
def user():
    # mycursor = mydb2.cursor(buffered = True)
    cnx1 = cnxpool.get_connection()
    mycursor = cnx1.cursor()
    # check signin
    if request.method == "GET":
        # if "email" in session:
        token = request.cookies.get("wehelp_user")
        if token:
            decoded_jwt = jwt.decode(token, key, algorithms="HS256")
            # email = session["email"]
            email = decoded_jwt["email"]
            sql = "SELECT id, name, email FROM members where email=%s"
            mycursor.execute(sql, (email,))  
            member_data = mycursor.fetchone()
            loggedin_api = {
                "data": {
                    "id": member_data[0],
                    "name": member_data[1],
                    "email": member_data[2]
                }
            }
        else:
            loggedin_api = {
                "data": None
            }
        mycursor.close()
        cnx1.close()
        return jsonify(loggedin_api)

# sign up
    elif request.method == "POST":
        request_data = request.get_json()
        name = request_data["name"]
        email = request_data["email"]
        password = request_data["password"]
        sql = "SELECT COUNT(*) FROM members WHERE email=%s"
        mycursor.execute(sql, (email,))
        data = mycursor.fetchone()
        if data[0] == 0:
            sql = "INSERT INTO members (name, email, password) VALUES (%s, %s, %s)"
            val = (name, email, password)
            mycursor.execute(sql, val)
            # mydb.commit()
            # do the commit in connection while using connection pool
            cnx1.commit()
            signup_api = {
                "ok": True
            }
        elif data[0] == 1:
            signup_api = {
                "error": True,
                "message": "註冊失敗，重複的 Email 或其他原因。"
            }
        else:
            signup_api = {
                "error": True,
                "message": "伺服器內部錯誤。"
            }
        mycursor.close()
        cnx1.close()
        return jsonify(signup_api)

# sign in
    elif request.method == "PATCH":
        request_data = request.get_json()
        email = request_data["email"]
        password = request_data["password"]
        sql = "SELECT COUNT(*) FROM members WHERE email=%s AND password=%s"
        mycursor.execute(sql, (email, password))
        data = mycursor.fetchone()
        if data[0] == 1:
            encoded_jwt = jwt.encode({"email": email}, key, algorithm="HS256")
            # session["email"] = email
            # session["password"] = password
            signin_api = {
                "ok": True
            }
            resp = make_response(signin_api)
            resp.set_cookie(key="wehelp_user", value=encoded_jwt, expires=time.time()+6*60)
            # return jsonify(signin_api)
            mycursor.close()
            cnx1.close()
            return resp
        elif data[0] == 0:
            signin_api = {
                "error": True,
                "message": "登入失敗，帳號或密碼錯誤或其他原因"
            }
            mycursor.close()
            cnx1.close()
            return jsonify(signin_api)
        else:
            signin_api = {
                "error": True,
                "message": "伺服器內部錯誤"
            }
            mycursor.close()
            cnx1.close()
            return jsonify(signin_api)
        

# log out
    elif request.method == "DELETE":
        # session.clear()
        loggedout_api = {
            "ok": True
        }
        resp = make_response(loggedout_api)
        resp.set_cookie("wehelp_user", "", expires=0)
        # return jsonify(loggedout_api)
        mycursor.close()
        cnx1.close()
        return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
    # app.debug = True
    # app.run(port=3000)
