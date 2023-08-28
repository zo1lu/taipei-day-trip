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
    cursor = con.cursor(dictionary=True)
    if keyword!=None:
        query = "SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id WHERE mrts.mrt_name like %s or site.name like %s"
        cursor.execute(query,(keyword,'%{}%'.format(keyword)))
    else:
        query="SELECT site.id, site.name, site.category, site.description, site.address, site.transport, mrts.mrt_name as mrt, site.latitude as lat, site.longitude as lng FROM attractions as site LEFT JOIN mrts ON site.mrt_id = mrts.id"
        cursor.execute(query)
    
    data = cursor.fetchall()
    size = len(data)
    result_data = []
    i = page*12
    while i < size:
        site = data[i]
        id = site["id"]
        img_url_list = get_image_url_list(id)
        new_site = { **site, "images":img_url_list}
        result_data.append(new_site)
        i+=1
    return {
			"nextPage":page+1 if size>(page+1)*12 else None,
			"data":result_data
		}

def get_image_url_list(id):
    con = mysql.connect(**DB_CONFIG)
    cursor = con.cursor(dictionary=True)
    query = "SELECT image_url FROM images WHERE attraction_id = %s"
    cursor.execute(query,(id,))
    img_url_list = cursor.fetchall()  
    list = []
    for url in img_url_list:
        list.append(url["image_url"])
    return list

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
    result_data = []
    for mrt in data:
        result_data.append(mrt["mrt_name"])
    return {"data":result_data}



