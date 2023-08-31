import os
import json
import mysql.connector as mysql

cur_path = os.path.dirname(__file__)
new_path = os.path.relpath('.\\taipei-attractions.json',cur_path)
file = open(new_path,encoding="utf-8")
data = json.load(file)
data = data["result"]["results"]

attraction_table = []
image_table = []
mrt_table = []

for site in data:
    # add new mrt name to mrt_table
    if ((site["MRT"]!=None) and (site["MRT"] not in mrt_table)):
        mrt_table.append(site["MRT"])
    
    mrt_id = mrt_table.index(site["MRT"])+1 if site["MRT"]!=None else None
    # add attraction data
    attraction_element = [  site["_id"],
                            site["name"],
                            site["CAT"],
                            site["description"],
                            site["address"],
                            site["direction"],
                            mrt_id,
                            site["latitude"],
                            site["longitude"]]
    attraction_table.append(attraction_element)

    # add image data
    list = site["file"].split("http")
    for url in list:
        suffixes = ("png","jpg")
        if url.lower().endswith(suffixes):
            image_table.append([site["_id"],"http"+url])

# print(attraction_table)
# print(image_table)
# print(mrt_table)


#Configuration for MySQL database
DB_CONFIG = {
    'user': "root",
    'password': 'admin',
    'host': '127.0.0.1',
    'database':'taipeitripweb'
}

con = mysql.connect(**DB_CONFIG)
for mrt in mrt_table:
    cursor = con.cursor()
    query = "INSERT INTO mrts (mrt_name) VALUES (%s)"
    cursor.execute(query, (mrt,))
    con.commit()
    cursor.close()

for site in attraction_table:
    cursor = con.cursor()
    query = "INSERT INTO attractions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (site[0], site[1], site[2], site[3], site[4], site[5], site[6], site[7], site[8]))
    con.commit()
    cursor.close()

for img in image_table:
    cursor = con.cursor();
    query = "INSERT INTO images(attraction_id, image_url) VALUES (%s, %s)"
    cursor.execute(query, (img[0], img[1]))
    con.commit()
    cursor.close()

con.close()
