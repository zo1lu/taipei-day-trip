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
    limit = 12

    if keyword!=None:
        query_data = "SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id WHERE mrts.mrt_name like %(precise_key)s OR site.name like %(fuzzy_key)s ORDER BY site.id LIMIT %(limit)s OFFSET %(start_index)s"
        parameter = {
            'precise_key':keyword,
            'fuzzy_key':'%{}%'.format(keyword),
            'limit':limit,
            'start_index':i
        }
        cursor_data.execute(query_data,parameter)
    else:
        query_data="SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id ORDER BY site.id LIMIT %(limit)s OFFSET %(start_index)s"
        parameter = {
            'limit':limit,
            'start_index':i
        }
        cursor_data.execute(query_data,parameter)

    data = cursor_data.fetchall()

    data_size = get_attractions_count(keyword)
    #get full site data of the page
    result_data = list(map(get_attraction_full_data,data))
    return {    
            "nextPage":int(page)+1 if data_size>(int(page)+1)*12 else None,
            "data":result_data
        }

def get_attractions_count(keyword):
    con = mysql.connect(**DB_CONFIG)
    cursor_data_count = con.cursor(dictionary=True)
    if keyword!=None:
        query_data_count = "SELECT COUNT(*) as size FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id WHERE mrts.mrt_name like %s OR site.name like %s"
        cursor_data_count.execute(query_data_count,(keyword,'%{}%'.format(keyword)))
    else:
        query_data_count = "SELECT COUNT(*) as size FROM attractions"
        cursor_data_count.execute(query_data_count)

    count = cursor_data_count.fetchone()
    data_size = count["size"]
    return data_size

def get_attraction_full_data(site_data):
    id = site_data["id"]
    return {**site_data, "images":get_image_url_list(id)}

def get_image_url_list(id):
    con = mysql.connect(**DB_CONFIG)
    cursor = con.cursor(dictionary=True)
    query = "SELECT image_url FROM images WHERE attraction_id = %s"
    cursor.execute(query,(id,))
    url_list = cursor.fetchall()  
    img_url_list = list(map(lambda url:url["image_url"],url_list))
    return img_url_list

def get_attraction_by_id(id):
    try:
        con = mysql.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)
        query = "SELECT * FROM attractions WHERE id = %s"
        cursor.execute(query, (id,))
        attraction = cursor.fetchone()
        return ({
            "data":{**attraction,"images":get_image_url_list(id)}
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
    query = "SELECT mrt_name FROM mrts INNER JOIN attractions as site ON site.mrt_id = mrts.id GROUP BY mrts.id ORDER BY COUNT(site.name) DESC LIMIT 40"
    cursor.execute(query)
    data = cursor.fetchall()
    result_data = list(map(lambda mrt:mrt["mrt_name"],data))
    return {"data":result_data}
