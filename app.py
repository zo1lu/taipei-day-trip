from flask import *
from models import get_attractions_by_page,get_attraction_by_id,get_mrts
app=Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.json.ensure_ascii = False

# Pages
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

#API
error_message = {
			"error": True,
			"message": "請按照情境提供對應的錯誤訊息"}
header = {
			"Access-Control-Allow-Origin" : "*"
		}

@app.route("/api/attractions")
def get_attractions_by_page_api():
	page = request.args.get("page")
	keyword = request.args.get("keyword")
	try:
		data = get_attractions_by_page(page,keyword)
		res = make_response(jsonify(data),200,header)
		return res
	except Exception as e:
		print(e)
		res= make_response(jsonify(error_message),500,header)
		return res

@app.route("/api/attraction/<attractionId>")
def get_attraction_by_id_api(attractionId):
	try:
		data = get_attraction_by_id(attractionId)
		status_code = 400 if data.get("error") else 200
		res = make_response(jsonify(data),status_code,status_code)
		return res
	except Exception as e:
		print(e)
		res= make_response(jsonify(error_message),500,header)
		return res

@app.route("/api/mrts")
def get_mrts_api():
	try:
		data = get_mrts()
		res = make_response(jsonify(data),200,header)
		return res
	except Exception as e:
		print(e)
		res= make_response(jsonify(error_message),500,header)
		return res

app.run(host="0.0.0.0", port=3000)