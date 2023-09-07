from flask import *
from routes.site_routes import site
from routes.api_routes import api

app=Flask(__name__,
			static_folder ="public",
			static_url_path = "/" )
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.json.ensure_ascii = False

app.register_blueprint(site)
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=3000)