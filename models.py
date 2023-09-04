import mysql.connector as mysql
from flask import *

#Configuration for MySQL database
DB_CONFIG = {
    'user': 'root',
    'password': 'admin',
    'host': '127.0.0.1',
    'database':'taipeitripweb'
}

def get_attractions_by_page(page,keyword):
    con = mysql.connect(**DB_CONFIG)
    cursor_data = con.cursor(dictionary=True)
    i = int(page)*12
    data_per_page = 12

    if keyword!=None:
        query_data = "SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng, GROUP_CONCAT(images.image_url) as images FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id JOIN images ON site.id = images.attraction_id WHERE mrts.mrt_name like %(precise_key)s OR site.name like %(fuzzy_key)s GROUP BY site.id ORDER BY site.id LIMIT %(data_per_page)s OFFSET %(start_index)s"
        parameter = {
            "precise_key":keyword,
            "fuzzy_key":"%{}%".format(keyword),
            "data_per_page":data_per_page,
            "start_index":i
        }
        cursor_data.execute(query_data,parameter)
    else:
        query_data="SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng, GROUP_CONCAT(images.image_url) as images FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id JOIN images ON site.id = images.attraction_id GROUP BY site.id ORDER BY site.id LIMIT %(data_per_page)s OFFSET %(start_index)s"
        parameter = {
            "data_per_page":data_per_page,
            "start_index":i
        }
        cursor_data.execute(query_data,parameter)

    data = cursor_data.fetchall()
    result_data = list(map(lambda site:{**site,"images":site["images"].split(",")},data))

    data_size = get_attractions_count(keyword)

    return {    
            "nextPage":int(page)+1 if data_size>(int(page)+1)*12 else None,
            "data":result_data
        }

def get_attractions_count(keyword):
    con = mysql.connect(**DB_CONFIG)
    cursor_data_count = con.cursor(dictionary=True)
    if keyword!=None:
        query_data_count = "SELECT COUNT(*) as size FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id WHERE mrts.mrt_name like %(precise_key)s OR site.name like %(fuzzy_key)s"
        parameter = {
            "precise_key":keyword,
            "fuzzy_key":"%{}%".format(keyword)
        }
        cursor_data_count.execute(query_data_count,parameter)
    else:
        query_data_count = "SELECT COUNT(*) as size FROM attractions"
        cursor_data_count.execute(query_data_count)

    count = cursor_data_count.fetchone()
    data_size = count["size"]
    return data_size

def get_attraction_by_id(id):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
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

# get_attraction_by_id(1)
# get_mrts();