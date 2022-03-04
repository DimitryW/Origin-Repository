from flask import *
import json
import mysql.connector

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False  # not to Sort the keys of JSON objects alphabetically

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vaapad666",
    database="wehelp2",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()


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
    page = request.args.get("page", default=0, type=int)
    keyword = request.args.get("keyword", default="")
    mycursor.execute(
        f"SELECT COUNT(*) FROM attractions WHERE name LIKE '%{keyword}%'")
    (total,) = mycursor.fetchone()
    for i in range(0, total, 12):
        if page == i/12:
            mycursor.execute(f"SELECT id, name, category, description, address, transport, mrt, latitude, longitude FROM attractions WHERE name LIKE '%{keyword}%' LIMIT {i}, 12")
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
    return jsonify(page_data)


@app.route("/api/attraction/<attractionId>")
def attract_id(attractionId):
    try:
        mycursor.execute(f"SELECT id, name, category, description, address, transport, mrt, latitude, longitude FROM attractions WHERE id = {attractionId}")
        attract_data = mycursor.fetchone()
        if mycursor.rowcount == 1:
            (id, name, category, description, address, transport, mrt, latitude, longitude) = attract_data
            mycursor.execute(
                f"SELECT img_url FROM photos WHERE attraction_id ={attractionId}")
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
    return jsonify(attract_info)


app.run(port=3000)
