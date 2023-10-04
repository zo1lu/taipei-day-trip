from flask import *
from models import get_attractions_by_page, get_attraction_by_id, get_mrts, encode_userdata,decode_token, validate_membership, create_account, create_error_message, create_booking, get_bookings, delete_booking, order_and_pay, get_order_full_data

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
		name = str(data["name"])
		email = str(data["email"])
		password = str(data["password"])
		result = create_account(name, password, email)
		if result:
			success_message = {"ok":True}
			res = make_response(jsonify(success_message),200,header)
			return res
		else:
			res = make_response(jsonify(create_error_message()),400,header)
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
		email = str(data["email"])
		password = str(data["password"])
		return_data = validate_membership(email, password)
		if return_data:
			user_id, user_name, user_email = return_data.values()
			token = {"token":encode_userdata(user_id, user_name, user_email)}
			res = make_response(jsonify(token),200,header)
			return res
		else:
			res = make_response(jsonify(create_error_message()),400,header)
			return res
	except Exception as e:
			print(e)
			res = make_response(jsonify(create_error_message()),500,header)
			return res

@api.route("/booking")
def get_bookings_list():
	try:
		token = request.headers.get('Authorization').split(" ")[1]
		validation_id = decode_token(token)["id"]
		if validation_id:
			bookings_list = get_bookings(validation_id)
			result_data = {"data":bookings_list}
			res = make_response(jsonify(result_data),200,header)
			return res
		else:
			res = make_response(jsonify(create_error_message()),403,header)
			return res
	except Exception as e:
		print(e)
		res = make_response(jsonify(create_error_message()),500,header)
		return res		

@api.route("/booking", methods=["POST"])
def create_booking_api():
	try:
		token = request.headers.get('Authorization').split(" ")[1]
		validation_id = decode_token(token)["id"]
		if validation_id:
			try:
				data = request.get_json()
				attraction_id = data["attractionId"]
				date = data["date"]
				time = data["time"]
				price = data["price"]
				create_booking(validation_id, attraction_id, date, time, price)
				success_message = {"ok":True}
				res = make_response(jsonify(success_message),200,header)
				return res
			except Exception as e:
				print(e)
				res = make_response(jsonify(create_error_message()),400,header)
				return res
		else:
			res = make_response(jsonify(create_error_message()),403,header)
			return res
	except Exception as e:
		print(e)
		res = make_response(jsonify(create_error_message()),500,header)
		return res

@api.route("/booking", methods = ["DELETE"])
def delete_booking_api():
	token = request.headers.get('Authorization').split(" ")[1]
	validation_id = decode_token(token)["id"]
	if validation_id:
		try:
			data = request.get_json()
			booking_id = data["bookingId"]
			delete_booking(booking_id)
			success_message = {"ok":True}
			res = make_response(jsonify(success_message),200,header)
			return res
		except Exception as e:
			print(e)
			res = make_response(jsonify(create_error_message()),400,header)
			return res
	else:
		res = make_response(jsonify(create_error_message()),403,header)
		return res
	
@api.route("/orders", methods=["POST"])
def create_order_api():
	try:
		token = request.headers.get('Authorization').split(" ")[1]
		validation_id = decode_token(token)["id"]
		if validation_id:
			try:
				data = request.get_json()
				prime = data["prime"]
				total_price = data["total_price"]
				#validate data here!
				name = data["contact"]["name"]
				email = data["contact"]["email"]
				phone = data["contact"]["phone"]
				result = {"data":order_and_pay(validation_id, prime, total_price, name, email, phone)}
				res = make_response(jsonify(result),200,header)
				return res
			except Exception as e:
				print(e)
				res = make_response(create_error_message(),400,header)
				return res
		else:
			res = make_response(create_error_message(),403,header)
			return res
	except Exception as e:
		print(e)
		res = make_response(create_error_message(),500,header)
		return res

@api.route("/order/<orderNumber>")
def get_order_by_order_number_api(orderNumber):
	try:
		token = request.headers.get('Authorization').split(" ")[1]
		validation_id = decode_token(token)["id"]
		if validation_id:
			result = {"data":get_order_full_data(orderNumber)}
			res = make_response(jsonify(result),200,header)
			return res
		else:
			res = make_response(create_error_message(),403,header)
			return res
	except Exception as e:
		print(e)
		res = make_response(create_error_message(),500,header)
		return res