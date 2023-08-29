import mysql.connector as mysql

#Configuration for MySQL database
DB_CONFIG = {
    'user': "root",
    'password': 'admin',
    'host': '127.0.0.1',
    'database':'taipeitripweb'
}

def get_attractions_by_page(page,keyword):
    con = mysql.connect(**DB_CONFIG)
    cursor_data = con.cursor(dictionary=True,buffered=True)
    cursor_data_count = con.cursor(dictionary=True,buffered=True)
    i = page*12
    if keyword!=None:
        query_data = "SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id WHERE mrts.mrt_name like %s OR site.name like %s LIMIT %s,12"
        cursor_data.execute(query_data,(keyword,'%{}%'.format(keyword),i))

        query_data_count = "SELECT COUNT(*) as size FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id WHERE mrts.mrt_name like %s OR site.name like %s"
        cursor_data_count.execute(query_data_count,(keyword,'%{}%'.format(keyword)))
    else:
        query_data="SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id LIMIT %s,12"
        cursor_data.execute(query_data,(i,))

        query_data_count = "SELECT COUNT(*) as size FROM attractions"
        cursor_data_count.execute(query_data_count)

    data = cursor_data.fetchall()
    count = cursor_data_count.fetchone()

    data_size = count["size"]

    #get full site data of the page
    result_data = list(map(get_attraction_full_data,data))

    return {    
			"nextPage":page+1 if data_size>(page+1)*12 else None,
			"data":result_data
		}


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
        cursor.execute(query, id)
        attraction = cursor.fetchone()
        return ({
            "data":{**attraction,"images":get_image_url_list(id)}
        })
    except:
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

get_attractions_by_page(4,None)