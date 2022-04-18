from email.policy import default
from flask import *
import jwt
import time
from model.model import AttractionDB, PhotosDB, MemberDB, OrdersDB
import requests
import json
import datetime
from dotenv import load_dotenv
import os
import re

load_dotenv()
jwt_key = os.getenv("jwt_key")
partner_key = os.getenv("partner_key")
merchant_id = os.getenv("merchant_id")
tappay_details = os.getenv("tappay_details")
x_api_key = os.getenv("x_api_key")


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False  # not to Sort the keys of JSON objects alphabetically


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

@app.route("/member")
def member():
    return render_template("member.html")


@app.route("/api/attractions")
def api_attractions():
    page = request.args.get("page", default=0, type=int)
    keyword = request.args.get("keyword", default="", type=str)
    (total,) = AttractionDB.search_name(keyword)
    if total > 0:
        for i in range(0, total, 12):
            if page == i/12:
                col_list = ['id', 'name', 'category', 'description', 'address', 'transport', 'mrt', 'latitude', 'longitude']
                db_data = AttractionDB.search_detail_by_name(keyword, col_list, index=i, limit=12)
                page_data = {
                    "nextPage": page+1 if page < (total//12) else None,
                    "data": []
                }
                for i in range(len(db_data)):
                    (attract_id, name, category, description, address, transport, mrt, latitude, longitude) = db_data[i]
                    img_urls = PhotosDB.search_img(attract_id)
                    images = []
                    for x in img_urls:
                        img = x[0]
                        images.append(img)
                    attract_info = {
                        "id": attract_id,
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
    return jsonify(page_data)


@app.route("/api/attraction/<attractionId>")
def attract_id(attractionId):
    try:
        col_list = ['id', 'name', 'category', 'description', 'address', 'transport', 'mrt', 'latitude', 'longitude']
        attract_data = AttractionDB.search_detail_by_id(attractionId, col_list)
        if len(attract_data) == 1:
            (attract_id, name, category, description, address, transport, mrt, latitude, longitude) = attract_data[0]
            img_urls = PhotosDB.search_img(attract_id)
            images = []
            for x in img_urls:
                img = x[0]
                images.append(img)
            attract_info = {
                "data": {
                    "id": attract_id,
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


@app.route("/api/user", methods=["GET", "POST", "PATCH", "DELETE"])
def user():
    if request.method == "GET":
        user_token = request.cookies.get("wehelp_user")
        if user_token:
            decoded_jwt = jwt.decode(user_token, jwt_key, algorithms=["HS256"])
            email = decoded_jwt["email"]
            member_data = MemberDB.search_member(email)
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
        return jsonify(loggedin_api), 200

# sign up
    elif request.method == "POST":
        request_data = request.get_json()
        name = request_data["name"]
        email = request_data["email"]
        password = request_data["password"]
        re_name = "^([\u4e00-\u9fa5]{2,20}|[a-zA-Z.\s]{2,20})$"
        re_email = "^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$"

        if (re.search(re_name, name)!=None) & (re.search(re_email, email)!=None):
            member_count = MemberDB.count_member(email)
        else:
            signup_api = {
                "error": True,
                "message": "註冊失敗，輸入格式錯誤。"
            }
            return jsonify(signup_api), 400

        if member_count == 0:
            MemberDB.create_member(name, email, password)
            signup_api = {
                "ok": True
            }
            return jsonify(signup_api), 200
        elif member_count == 1:
            signup_api = {
                "error": True,
                "message": "註冊失敗，重複的 Email 或其他原因。"
            }
            return jsonify(signup_api), 400
        else:
            signup_api = {
                "error": True,
                "message": "伺服器內部錯誤。"
            }
            return jsonify(signup_api), 500
        
# sign in
    elif request.method == "PATCH":
        request_data = request.get_json()
        email = request_data["email"]
        password = request_data["password"]
        data = MemberDB.check_member(email, password)
        if data == 1:
            encoded_jwt = jwt.encode({"email": email}, jwt_key, algorithm="HS256")
            signin_api = {
                "ok": True
            }
            resp = make_response((signin_api),200)
            resp.set_cookie(key="wehelp_user", value=encoded_jwt, expires=time.time()+60*60)
            return resp
        elif data == 0:
            signin_api = {
                "error": True,
                "message": "登入失敗，帳號或密碼錯誤或其他原因"
            }
            return jsonify(signin_api), 400
        else:
            signin_api = {
                "error": True,
                "message": "伺服器內部錯誤"
            }
            return jsonify(signin_api), 500
        
# log out
    elif request.method == "DELETE":
        loggedout_api = {
            "ok": True
        }
        resp = make_response((loggedout_api), 200)
        resp.set_cookie("wehelp_user", "", expires=0)
        return resp


@app.route("/api/booking", methods=["GET", "POST", "DELETE"])
def api_booking():
    user_token = request.cookies.get("wehelp_user")
    booking_token = request.cookies.get("wehelp_booking")
    if request.method == "GET":
        if user_token:
            decoded_booking_jwt = jwt.decode(booking_token, jwt_key, algorithms=["HS256"])
            col_list = ["name", "address"]
            attraction_data = AttractionDB.search_detail_by_id(decoded_booking_jwt["id"], col_list)
            img_urls = PhotosDB.search_img(decoded_booking_jwt["id"])
            booking_api = {
            "data": {
                "attraction": {
                "id": decoded_booking_jwt["id"],
                "name": attraction_data[0][0],
                "address": attraction_data[0][1],
                "image": img_urls[0]
                },
                "date": decoded_booking_jwt["date"],
                "time": decoded_booking_jwt["time"],
                "price": decoded_booking_jwt["price"]
                }
            }
            return jsonify(booking_api), 200
        else:
            booking_api = {
                "error": True,
                "message": "未登入系統，拒絕存取"
                }
            return jsonify(booking_api), 403
    elif request.method == "POST":
        request_data = request.get_json()
        attract_id = request_data["attractionId"]
        date = request_data["date"]
        travel_time = request_data["time"]
        price = request_data["price"]
        try:
            if user_token:
                if date != "":
                    booking_api = {
                    "ok": True
                    }
                    jwt_booking_data = {
                        "id": attract_id,
                        "date":date,
                        "time":travel_time, # 注意變數名稱不要跟 time 重複
                        "price":price
                    }
                    encoded_jwt = jwt.encode(jwt_booking_data, jwt_key, algorithm="HS256")
                    resp = make_response((booking_api), 200)
                    resp.set_cookie("wehelp_booking", encoded_jwt, expires=time.time()+60*60)
                    return resp
                else:
                    booking_api = {
                        "error": True,
                        "message": "建立失敗，輸入不正確或其他原因"
                        }
                    return jsonify(booking_api), 400    
            else:
                booking_api = {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                    }
                return jsonify(booking_api), 403
        except:
            booking_api = {
                    "error": True,
                    "message": "伺服器內部錯誤"
                    }
            return jsonify(booking_api), 500
        
    elif request.method == "DELETE":
        if user_token:
                booking_api = {
                    "ok": True
                    }
                resp = make_response(jsonify(booking_api), 200) 
                resp.set_cookie("wehelp_booking", "", expires=0)
                return resp
        else:
            booking_api = {
                "error": True,
                "message": "未登入系統，拒絕存取"
                }
            return jsonify(booking_api), 403
    
@app.route("/api/orders", methods=["POST"])
def receive_order():
    user_token = request.cookies.get("wehelp_user")
    try:
        if user_token:
            decoded_jwt = jwt.decode(user_token, jwt_key, algorithms=["HS256"])
            member_email = decoded_jwt["email"]
            order_data = request.get_json()
            prime = order_data["prime"]
            amount = order_data["order"]["price"]
            name = order_data["order"]["contact"]["name"]
            email = order_data["order"]["contact"]["email"]
            phone = order_data["order"]["contact"]["phone"]
            member_id = MemberDB.search_member(member_email)[0]
            attract_id = order_data["order"]["trip"]["attraction"]["id"]
            attract_name = order_data["order"]["trip"]["attraction"]["name"]
            date = order_data["order"]["trip"]["date"]
            order_no = str(member_id) + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

            re_name = "^([\u4e00-\u9fa5]{2,20}|[a-zA-Z.\s]{2,20})$"
            re_email = "^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$"
            re_phone = "^09[0-9]{8}$"
            if (re.search(re_name, name)!=None) & (re.search(re_email, email)!=None) & (re.search(re_phone, phone)!=None):
                OrdersDB.create_order(member_id, attract_id, attract_name, date, amount, name, email, phone, order_no)
            else:
                order_response = {
                    "error": True,
                    "message": "訂單建立失敗，輸入格式錯誤。"
                    }
                return jsonify(order_response), 400

            url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
            myobj = {
                "prime": prime,
                "partner_key": partner_key,
                "merchant_id": merchant_id,
                "details": tappay_details,
                "amount": amount,
                "cardholder": {
                    "phone_number": phone,
                    "name": name,
                    "email": email,
                },
                "remember": True
            }
            header = {
                "Content-Type": "application/json",
                "x-api-key": x_api_key}
            response = requests.post(url, json=myobj, headers=header)
            tappay_response = json.loads(response.text)

            if tappay_response["status"]==0:
                OrdersDB.pay_order(order_no)
                order_response = {
                    "data": {
                        "number": order_no,
                        "payment": {
                        "status": 0,
                        "message": "付款成功"
                        }
                    }
                    }
                return jsonify(order_response), 200
            else:
                order_response = {
                    "error": True,
                    "message": "訂單建立失敗，輸入不正確或其他原因"
                    }
                return jsonify(order_response), 400
        else:
            order_response = {
                "error": True,
                "message": "未登入系統，拒絕存取"
                }
            return jsonify(order_response), 403
    except:
        order_response = {
            "error": True,
            "message": "伺服器內部錯誤"
            }
        return jsonify(order_response), 500

@app.route("/api/order/<order_no>", methods=["GET"])
def check_order(order_no):
    user_token = request.cookies.get("wehelp_user")
    if user_token:
        (price, attract_id, date, name, email, phone, payment) = OrdersDB.check_order(order_no)
        (site_name, address) = AttractionDB.search_detail_by_id(attract_id, ["name", "address"])[0]
        img = PhotosDB.search_img(attract_id)[0]
        res ={
            "data": {
                "number": order_no,
                "price": price,
                "trip": {
                    "attraction": {
                        "id": attract_id,
                        "name": site_name,
                        "address": address,
                        "image": img
                        },
                    "date": date,
                    "time": "morning" if price==2000 else "afternoon"
                    },
                "contact": {
                    "name": name,
                    "email": email,
                    "phone": phone
                    },
                "status": 0 if payment=="paid" else 1
            }
            }
        return jsonify(res), 200
    res = {
        "error": True,
        "message": "未登入系統，拒絕存取"
        }
    return jsonify(res), 403

@app.route("/api/member_orders", methods=["GET"])
def member_order():
    user_token = request.cookies.get("wehelp_user")
    if user_token:
        decoded_jwt = jwt.decode(user_token, jwt_key, algorithms=["HS256"])
        email = decoded_jwt["email"]
        member_data = MemberDB.search_member(email)
        result = OrdersDB.check_order_by_member(member_data[0])
        member_orders ={
                "member_id": member_data[0],
                "member_name": member_data[1],
                "member_email": email,
                "data": []
                }
        for i in range(len(result)):
            date = result[i][0].split("-")[-2]
            order_info = {
                "order_number": result[i][0],
                "price": result[i][1],
                "payment": result[i][8],
                "attraction_id": result[i][2],
                "attraction": result[i][3],
                "date": result[i][4],
                "time": "早上9點到中午12點" if result[i][1]==2000 else "下午1點到下午5點",
                "contact_name": result[i][5],
                "contact_email": result[i][6],
                "contact_phone": result[i][7],
                "order_place_date": date[0:4] + "-" + date[4:6] + "-" + date[6:8]
            }
            member_orders["data"].append(order_info)
        return jsonify(member_orders), 200
        
    else:
        member_response = {
                "error": True,
                "message": "未登入系統，拒絕存取"
                }
        return jsonify(member_response), 403



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
    # app.debug = True
    # app.run(port=3000)


