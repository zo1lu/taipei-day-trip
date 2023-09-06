from flask import *

site = Blueprint('site',__name__)

# Pages
@site.route("/")
def index():
	return render_template("index.html")
@site.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@site.route("/booking")
def booking():
	return render_template("booking.html")
@site.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")