from flask import *
from models import get_attractions_by_page,get_attraction_by_id,get_mrts,encode_userdata,decode_token,validate_membership,create_account,create_error_message

api = Blueprint('api',__name__,url_prefix='/api')
#API
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
		res= make_response(jsonify(create_error_message()),500,header)
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
		res= make_response(jsonify(create_error_message()),500,header)
		return res

@api.route("/mrts")
def get_mrts_api():
	try:
		data = get_mrts()
		res = make_response(jsonify(data),200,header)
		return res
	except Exception as e:
		print(e)
		res= make_response(jsonify(create_error_message()),500,header)
		return res
	
@api.route("/user", methods=["POST"])
def create_member():
	try:
		data = request.get_json()
		name = data["name"]
		email = data["email"]
		password = data["password"]
		result = create_account(name, password, email)
		if result:
			success_message = {"ok":True}
			res = make_response(jsonify(success_message),200,header)
			return res
		else:
			res = make_response(jsonify(create_error_message("註冊失敗")),400,header)
			return res
	except Exception as e:
		print(e)
		res = make_response(jsonify(create_error_message()),500,header)
		return res

@api.route("/user/auth")
def get_member_info():
	token = request.headers.get('Authorization').split(" ")[1]
	validation = decode_token(token)
	user_data = {"data":validation if validation else None}
	res = make_response(jsonify(user_data),200,header)
	return res

@api.route("/user/auth", methods=["PUT"])
def log_in():
	try:
		data = request.get_json()
		email = data["email"]
		password = data["password"]
		return_data = validate_membership(email, password)
		if return_data:
			user_id, user_name, user_email = return_data.values()
			token = {"token":encode_userdata(user_id, user_name, user_email)}
			res = make_response(jsonify(token),200,header)
			return res
		else:
			res = make_response(jsonify(create_error_message("登入失敗")),400,header)
			return res
	except Exception as e:
			print(e)
			res = make_response(jsonify(create_error_message()),500,header)
			return res
