import mysql.connector
import mysql.connector.pooling
from config import dbconfig

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool", pool_size = 5, pool_reset_session=True, **dbconfig)

cnx1 = cnxpool.get_connection()
mycursor = cnx1.cursor()
mycursor.execute("SELECT COUNT(*) FROM attractions")
attraction_limit = mycursor.fetchone()[0]
mycursor.close()
cnx1.close()

class AttractionDB:
    @staticmethod        
    def search_name(name):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        mycursor.execute("SELECT COUNT(*) FROM attractions WHERE name LIKE %s", (f'%{name}%',))
        result = mycursor.fetchone()
        mycursor.close()
        cnx1.close()
        return result
    @staticmethod    
    def search_detail_by_name(name, col_list, index=0, limit=attraction_limit, ):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        sql = "SELECT "+ ",".join(col_list) + " FROM attractions WHERE name LIKE  %s LIMIT %s, " + f"{limit}" 
        mycursor.execute(sql, (f'%{name}%', index))
        attraction_data = mycursor.fetchall()
        mycursor.close()
        cnx1.close()
        return attraction_data
    @staticmethod    
    def search_detail_by_id(attract_id, col_list, index=0, limit=attraction_limit, ):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        sql = "SELECT "+ ",".join(col_list) + " FROM attractions WHERE id=%s LIMIT %s, " + f"{limit}" 
        mycursor.execute(sql, (attract_id, index))
        attraction_data = mycursor.fetchall()
        mycursor.close()
        cnx1.close()
        return attraction_data


class PhotosDB:
    @staticmethod    
    def search_img(attract_id):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        mycursor.execute("SELECT img_url FROM photos WHERE attraction_id =%s", (attract_id,))
        img_urls = mycursor.fetchall()
        mycursor.close()
        cnx1.close()
        return img_urls


class MemberDB:
    @staticmethod    
    def search_member(email):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        mycursor.execute("SELECT id, name, email FROM members where email=%s", (email,))  
        member_data = mycursor.fetchone()
        mycursor.close()
        cnx1.close()
        return member_data
    @staticmethod    
    def search_member_by_id(member_id):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        mycursor.execute("SELECT id, name, email FROM members where id=%s", (member_id,))  
        member_data = mycursor.fetchone()
        mycursor.close()
        cnx1.close()
        return member_data
    @staticmethod    
    def count_member(email):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        mycursor.execute("SELECT COUNT(*) FROM members where email=%s", (email,))  
        member_count = mycursor.fetchone()[0]
        mycursor.close()
        cnx1.close()
        return member_count
    @staticmethod    
    def create_member(name, email, password):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        sql = "INSERT INTO members (name, email, password) VALUES (%s, %s, %s)"
        val = (name, email, password)
        mycursor.execute(sql, val)
        cnx1.commit()
        mycursor.close()
        cnx1.close()
        return
    @staticmethod    
    def check_member(email, password):
        cnx1 = cnxpool.get_connection()
        mycursor = cnx1.cursor()
        sql = "SELECT COUNT(*) FROM members WHERE email=%s AND password=%s"
        mycursor.execute(sql, (email, password))
        data = mycursor.fetchone()[0]
        mycursor.close()
        cnx1.close()
        return data

class OrdersDB:
    @staticmethod
    def create_order(member_id, attract_id, attract_name, date, price, name, email, phone, order_no):
        cnx1 = cnxpool.get_connection()
        cursor = cnx1.cursor()
        sql = "INSERT INTO orders (member_id, attract_id, attract_name, date, price, name, email, phone, order_no) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (member_id, attract_id, attract_name, date, price, name, email, phone, order_no)
        cursor.execute(sql, val)
        cnx1.commit()
        cursor.close()
        cnx1.close()
        return
    @staticmethod
    def pay_order(order_no):
        cnx1 = cnxpool.get_connection()
        cursor = cnx1.cursor()
        cursor.execute("UPDATE orders SET payment='paid' Where order_no = %s", (order_no,))
        cnx1.commit()
        cursor.close()
        cnx1.close()
        return
    @staticmethod
    def check_order(order_no):
        cnx1 = cnxpool.get_connection()
        cursor = cnx1.cursor()
        sql = "SELECT price, attract_id, date, name, email, phone, payment FROM orders WHERE order_no=%s"
        cursor.execute(sql, (order_no,))
        result = cursor.fetchone()
        cursor.close()
        cnx1.close()
        return result
    def check_order_by_member(member_id, index=0, limit=1000):
        cnx1 = cnxpool.get_connection()
        cursor = cnx1.cursor()
        sql = "SELECT order_no, price, attract_id, attract_name, date, name, email, phone, payment FROM orders WHERE member_id=%s LIMIT %s, %s"
        cursor.execute(sql, (member_id, index, limit))
        result = cursor.fetchall()
        cursor.close()
        cnx1.close()
        return result



