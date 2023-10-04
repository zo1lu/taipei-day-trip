import mysql.connector as mysql
from flask import *
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, date
import requests
import string
import random
load_dotenv()
#Configuration for MySQL database
DB_CONFIG = {
    'user': os.getenv("DBUSER"),
    'password': os.getenv("DBPASSWORD"),
    'host': os.getenv("DBHOST"),
    'database': os.getenv("DBDATABASE")
}
#secret key for jwt
key=os.getenv("JWTKEY")

def get_attactions_with_keyword(keyword, start_index, data_num):
    con = mysql.connect(**DB_CONFIG)
    cursor_data = con.cursor(dictionary=True)
    query_data = "SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng, GROUP_CONCAT(images.image_url) as images FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id JOIN images ON site.id = images.attraction_id WHERE mrts.mrt_name like %(precise_key)s OR site.name like %(fuzzy_key)s GROUP BY site.id ORDER BY site.id LIMIT %(data_num)s OFFSET %(start_index)s"
    parameter = {
        "precise_key":keyword,
        "fuzzy_key":"%{}%".format(keyword),
        "data_num":data_num,
        "start_index":start_index
    }
    cursor_data.execute(query_data, parameter)
    data = cursor_data.fetchall()
    return data

def get_attractions_without_keyword(start_index, data_num):
    con = mysql.connect(**DB_CONFIG)
    cursor_data = con.cursor(dictionary=True)
    query_data="SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng, GROUP_CONCAT(images.image_url) as images FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id JOIN images ON site.id = images.attraction_id GROUP BY site.id ORDER BY site.id LIMIT %(data_num)s OFFSET %(start_index)s"
    parameter = {
        "data_num":data_num,
        "start_index":start_index
    }
    cursor_data.execute(query_data, parameter)
    data = cursor_data.fetchall()
    return data

def get_attractions_by_page(page,keyword):
    if keyword!=None:
        data = get_attactions_with_keyword(keyword,int(page)*12,12)
        #check next page data existance
        next_page_data = get_attactions_with_keyword(keyword,(int(page)+1)*12,1)
    else:
        data = get_attractions_without_keyword(int(page)*12,12)
        #check next page data existance
        next_page_data = get_attractions_without_keyword((int(page)+1)*12,1)

    result_data = list(map(lambda site:{**site,"images":site["images"].split(",")},data))

    return {    
            "nextPage":int(page)+1 if len(next_page_data)==1 else None,
            "data":result_data
        }

def get_attraction_by_id(id):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        cursor.execute("SET SESSION group_concat_max_len = 5000")
        query = "SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt,  site.latitude as lat, site.longitude as lng, GROUP_CONCAT(images.image_url) as images FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id JOIN images ON site.id = images.attraction_id WHERE site.id = %s GROUP BY site.id "
        cursor.execute(query, (id,))
        attraction_data = cursor.fetchone()
        result_data = {**attraction_data, "images":attraction_data["images"].split(",") }
        return ({
            "data":result_data
        })
    except Exception as e:
        print(e)
        return({
            "error": True,
            "message": "請按照情境提供對應的錯誤訊息"
        })
    
def get_mrts():
    con = mysql.connect(**DB_CONFIG)
    cursor = con.cursor(dictionary=True)
    query = "SELECT mrt_name FROM mrts JOIN attractions as site ON site.mrt_id = mrts.id GROUP BY mrts.id ORDER BY COUNT(site.name) DESC LIMIT 40"
    cursor.execute(query)
    data = cursor.fetchall()
    result_data = list(map(lambda mrt:mrt["mrt_name"],data))
    return {"data":result_data}

def validate_email(email):
    con = mysql.connect(**DB_CONFIG)
    cursor = con.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email=%s"
    cursor.execute(query,(email,))
    email_validate = cursor.fetchone()
    result = False if email_validate else True
    return result

def create_account(username,password,email):
    if validate_email(email)==False:
        return False
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        # how to know if creation fail
        cursor.execute(query,(username, password, email))
        con.commit()
        return True
    except Exception as e:
        print(e)
        return False
    

def validate_membership(email,password):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "SELECT id, username, email FROM users WHERE email=%s and password=%s"
        cursor.execute(query,(email,password))
        userdata = cursor.fetchone()
        return userdata if userdata else False
    except Exception as e:
        print(e)
        return False

def encode_userdata(user_id,username,email):
    expire_date = datetime.now() + timedelta(days = 7)
    encoded = jwt.encode({"exp":expire_date, "id":user_id, "name":username, "email":email}, key,algorithm="HS256")
    return encoded

def decode_token(token):
    try:
        decoded = jwt.decode(token, key, algorithms="HS256")
        exp, id, name, email = decoded.values()
        user_data = {"id":id, "name":name, "email":email}
        return user_data
    except jwt.ExpiredSignatureError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False

def create_error_message():
    return{
        "error": True,
        "message": "請按照情境提供對應的錯誤訊息"}

def get_bookings(user_id):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "SELECT id, attraction_id as site_id, date, time, price FROM bookings WHERE user_id = %s and ordered = false"
        cursor.execute(query,(user_id,))
        bookings = cursor.fetchall()
        result = list(map(lambda book:{**book, "date": book["date"].strftime('%Y-%m-%d'), "attraction":get_attraction_data(book["site_id"])}, bookings))
        return result
    except Exception as e:
        print(e);
        return False
    
def get_attraction_data(attraction_id):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "SELECT site.id as id, site.name as name, site.address as address, img.image_url as image FROM attractions as site LEFT JOIN images as img ON img.attraction_id = site.id WHERE site.id = %s LIMIT 1;"
        cursor.execute(query,(attraction_id,))
        attraction_data = cursor.fetchone()
        return attraction_data
    except Exception as e:
        print(e);
        return False
    
def create_booking(user_id, attraction_id, date, time, price):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "INSERT INTO bookings (user_id, attraction_id, date, time, price) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query,(user_id, attraction_id, date, time, price))
        con.commit()
    except Exception as e:
        print(e)
        return False
    
def delete_booking(booking_id):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "DELETE FROM bookings WHERE id = %s"
        cursor.execute(query,(booking_id,))
        con.commit()
    except Exception as e:
        print(e)
        return False

def create_order_data(user_id, total_price, name, email, phone):
    # add order data into database
    # alter orders database table
    try:
        order_number = create_order_number()
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "INSERT INTO orders (user_id, order_number, price, name, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query,(user_id, order_number, total_price, name, email, phone))
        con.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        order_id = cursor.fetchone()["LAST_INSERT_ID()"]
        return {"order_id":order_id, "order_number":order_number}
    except Exception as e:
        print("create order data error:",e)
        return False

def update_bookings_order_id(user_id, order_id):
    # find all the unorderd booking of the user?
    # Or pass all the bookingId that are going to ordered?
    # add order_id and change ordered to true 
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "UPDATE bookings SET order_id = %s, ordered = 1 WHERE user_id = %s AND ordered = 0"
        cursor.execute(query,(order_id, user_id))
        con.commit()
    except Exception as e:
        print("update bookings order id error",e)
        return False

def create_order_number():
    N = 5
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    order_number = 'TTO' + date.today().strftime("%y%m%d") + random_str
    return order_number

def pay_order(prime, total_price, card_holder):
    #send request to tappar server
    try:
        url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        partner_key = os.getenv("PARTNERKEY")
        head = {
            "Content-Type":"application/json",
            "x-api-key": partner_key
        }
        body = {
            "prime": prime,
            "partner_key": partner_key,
            "merchant_id": "zo1lu_ESUN",
            "details": "TapPay Test",
            "amount": total_price,
            "cardholder": card_holder,
            "remember": False
        }
        response = requests.post(url, headers = head, json = body)
        print(response)
        return response
    except Exception as e:
        print("pay order error",e)
        return False
    #send request
    #get response
    #return response
    
def update_payment_status(order_id, status):
    try:
        paid = 1 if status==0 else 0
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "UPDATE orders SET paid = %s WHERE id = %s"
        cursor.execute(query,(paid, order_id))
        con.commit()
    except Exception as e:
        print("Update payment status",e)
        return False

def order_and_pay(user_id, prime, total_price, name, email, phone):
    try:
        order_data = create_order_data(user_id, total_price, name, email, phone)
        order_id = order_data["order_id"]
        order_number = order_data["order_number"]
        if order_id:
            update_bookings_order_id(user_id, order_id)
            card_holder = {
                "phone_number":phone,
                "name":name,
                "email":email
            }
            response = pay_order(prime, total_price, card_holder)
            result = response.json()
            update_payment_status(order_id, result["status"])
            return_data = {
                "number":order_number,
                "payment":{
                    "status":result["status"],
                    "message":result["msg"]
                }
            }
            return return_data
    except Exception as e:
        print("order and pay error",e)
        return False

def get_order_by_order_number(order_number):
    #get order and details by order number
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "SELECT id, order_number, price, JSON_OBJECT('name', name,'email', email,'phone', phone) as contact, created_time, paid as status FROM orders WHERE order_number = %s"
        cursor.execute(query,(order_number,))
        order = cursor.fetchone()
        result = {**order, "created_time": order["created_time"].strftime('%Y-%m-%d')}
        return result
    except Exception as e:
        print("1: ",e)

def get_booking_detail_by_orderId(order_id):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "SELECT book.attraction_id, site.name, site.address, img.image_url as image, book.date, book.time, book.price FROM bookings AS book LEFT JOIN attractions AS site ON book.attraction_id = site.id JOIN (SELECT attraction_id, MIN(id) AS min_image_id FROM images GROUP BY attraction_id) AS min_images ON site.id = min_images.attraction_id JOIN images AS img ON min_images.min_image_id = img.id WHERE order_id = %s"
        cursor.execute(query,(order_id,))
        bookings = cursor.fetchall()
        result = list(map(lambda book:{**book, "date": book["date"].strftime('%Y-%m-%d')}, bookings))
        return result
    except Exception as e:
        print("2: ",e)
    
# create_order_data(1, 9000, "test", "test@gmail.com", "0912345678")
def get_order_full_data(order_number):
    try:
        order_data = get_order_by_order_number(order_number)
        tour_data = get_booking_detail_by_orderId(order_data["id"])
        full_data = {**order_data,"trip":tour_data}
        # print(full_data)
        return full_data
    except Exception as e:
        print("3: ",e)

# get_order_full_data("TTO231003372YH")

