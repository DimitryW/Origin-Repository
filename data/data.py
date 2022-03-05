import json
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vaapad666",
    database="wehelp2"
)

mycursor = mydb.cursor()

with open("data/taipei-attractions.json", "r", encoding="utf-8") as file:  # 以 UTF-8 讀取的檔案
    data = json.load(file)

# 將資料載入TABLE attractions 
for i in data["result"]["results"]:
    sql = "INSERT INTO attractions (name, category, description, address, transport, mrt, latitude, longitude) values(%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (i["stitle"], i["CAT2"], i["xbody"], i["address"], i["info"], i["MRT"], i["latitude"], i["longitude"])
    mycursor.execute(sql, val)
    mydb.commit()


def pic_list(i=0, data=data):
    name = data["result"]["results"][i]["stitle"]
    url_list = []
    url_txt = data["result"]["results"][i]["file"].lower().split("http")
    for j in range(1, len(url_txt)):
        if url_txt[j].endswith("jpg") or url_txt[j].endswith("png"):
            url = "http" + url_txt[j]
            url_list.append(url)
    return name, url_list


# 將資料載入TABLE photos 
for i in range(len(data["result"]["results"])):
    name, url_list = pic_list(i)
    for j in range(len(url_list)):
        mycursor.execute(f"SELECT id FROM attractions WHERE name='{name}'")
        id = mycursor.fetchone()[0]
        sql = "INSERT INTO photos (attraction_id, name, img_url) VALUES(%s, %s, %s)"
        val = (id, name, url_list[j])
        mycursor.execute(sql, val)
        mydb.commit()


mycursor.close()
mydb.close()



