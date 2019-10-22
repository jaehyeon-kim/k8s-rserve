from flask_restplus._http import HTTPStatus


class BaseError(Exception):
    def __init__(self, code, description, http_status=HTTPStatus.INTERNAL_SERVER_ERROR):
        self.code = code if code else http_status.__dict__["phrase"]
        self.description = description if description else http_status.__dict__["description"]
        self.http_status = http_status

    @classmethod
    def fromStatusCode(cls, status_code):
        try:
            http_status = HTTPStatus(status_code)
        except Exception:
            http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        code = http_status.__dict__["phrase"]
        description = http_status.__dict__["description"]
        return cls(code, description, http_status)

    def resp(self):
        return {"error": {"code": self.code, "description": self.description}}


class Unauthorized(BaseError):
    def __init__(self, code=None, description=None, http_status=HTTPStatus.UNAUTHORIZED):
        BaseError.__init__(self, code, description, http_status)


class BadRequest(BaseError):
    def __init__(self, code=None, description=None, http_status=HTTPStatus.BAD_REQUEST):
        BaseError.__init__(self, code, description, http_status)


class NotFound(BaseError):
    def __init__(self, code=None, description=None, http_status=HTTPStatus.NOT_FOUND):
        BaseError.__init__(self, code, description, http_status)


class InternalServerError(BaseError):
    def __init__(self, code=None, description=None, http_status=HTTPStatus.INTERNAL_SERVER_ERROR):
        BaseError.__init__(self, code, description, http_status)
