from flask import *
from models import get_attractions_by_page,get_attraction_by_id,get_mrts

api = Blueprint('api',__name__,url_prefix='/api')
#API
error_message = {
			"error": True,
			"message": "請按照情境提供對應的錯誤訊息"}
header = {
			"Access-Control-Allow-Origin" : "*"
		}

@api.route("/attractions")
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

@api.route("/attraction/<attractionId>")
def get_attraction_by_id_api(attractionId):
	try:
		data = get_attraction_by_id(attractionId)
		status_code = 400 if data.get("error") else 200
		res = make_response(jsonify(data),status_code,header)
		return res
	except Exception as e:
		print(e)
		res= make_response(jsonify(error_message),500,header)
		return res

@api.route("/mrts")
def get_mrts_api():
	try:
		data = get_mrts()
		res = make_response(jsonify(data),200,header)
		return res
	except Exception as e:
		print(e)
		res= make_response(jsonify(error_message),500,header)
		return res