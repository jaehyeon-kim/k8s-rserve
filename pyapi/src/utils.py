from flask import request, current_app, g
from jose import jwt
from functools import wraps
from custom_errors import Unauthorized


class Auth(object):
    def get_token(self, username, password=None):
        claims = {"sub": username}
        access_token = jwt.encode(
            claims, current_app.config["JWT_SECRET"], algorithm=current_app.config["ALGORITHM"]
        )

        return {"access_token": access_token}

    @staticmethod
    def validate_token():
        if request.method != "OPTIONS":
            auth = request.headers.get("Authorization", None)
            if not auth:
                raise Unauthorized(
                    "Missing Authorization Header", "Authorization header is expected"
                )

            parts = auth.split()
            if parts[0].lower() != "bearer":
                raise Unauthorized("Invalid Header", "Authorization header must start with Bearer")
            elif len(parts) == 1:
                raise Unauthorized("Invalid Header", "Token not found")
            elif len(parts) > 2:
                raise Unauthorized("Invalid Header", "Authorization header must be Bearer token")

            token = parts[1]

            claims = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=[current_app.config["ALGORITHM"]],
            )
            return claims


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        claims = Auth.validate_token()
        if claims["sub"] != current_app.config["VALID_USER"]:
            raise Unauthorized(description="Invalid user")
        g.user = claims["sub"]
        return f(*args, **kwargs)

    return decorated_function
