import os
from flask import Flask, jsonify, current_app
from flask_cors import CORS
from flask_restplus import Api, Namespace, Resource, marshal, fields
from werkzeug.exceptions import HTTPException
import requests
from src.custom_errors import BaseError
from src.utils import Auth, login_required

## app configuration
app = Flask(__name__)
app.config.from_mapping(
    JWT_SECRET=os.getenv("JWT_SECRET", "myJwtSecret"),
    ALGORITHM=os.getenv("JWT_SECRET", "HS256"),
    VALID_USER=os.getenv("VALID_USER", "rserve"),
    RSERVE_HOST=os.getenv("RSERVE_HOST", "http://localhost:8000"),
)
app.url_map.strict_slashes = False
app.config.setdefault("RESTPLUS_MASK_HEADER", "X-Fields")
app.config.setdefault("RESTPLUS_MASK_SWAGGER", False)
cors = CORS(app, resources={"*": {"origins": "*"}})


@app.errorhandler(HTTPException)
def handle_error(err):
    e = BaseError.fromStatusCode(err.code)
    return e.resp(), e.http_status.value


## resources
ns = Namespace("demo", description="Demo namespace")


@ns.route("/login/<string:username>")
class LoginDebug(Resource):
    def get(self, username):
        return jsonify({"access_token": Auth().get_token(username=username)})


@ns.route("/test")
class RserveTest(Resource):
    @login_required
    def get(self):
        url = "{0}/{1}".format(current_app.config["RSERVE_HOST"], "test")
        return requests.get(url)


## api configuration
class UpdatedApi(Api):
    def handle_error(self, e):
        return e.resp(), e.http_status.value


api = UpdatedApi(title="rserve demo api", version="1.0", prefix="/api", errors=BaseError)
api.add_namespace(ns, "/demo")
api.init_app(app)

if __name__ == "__main__":
    if not os.getenv("FLASK_ENV"):
        os.environ["FLASK_ENV"] = "development"

    app.run(debug=True, host="0.0.0.0", port=os.getenv("CONTAINER_PORT", "5000"))
