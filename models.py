import mysql.connector as mysql
from flask import *
import os
from dotenv import load_dotenv
load_dotenv()
#Configuration for MySQL database
DB_CONFIG = {
    'user': os.getenv("DBUSER"),
    'password': os.getenv("DBPASSWORD"),
    'host': os.getenv("DBHOST"),
    'database': os.getenv("DBDATABASE")
}
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

