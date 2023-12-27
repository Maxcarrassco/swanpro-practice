from flask import Flask
from flask_cors import CORS
import json
from models import storage
from api.v1.routers.user_router import user_router
from api.v1.routers.class_router import class_router
from api.v1.routers.subject_router import subject_router
from api.v1.routers.auth_router import auth_router
from api.v1.routers.grade_router import grade_router

app = Flask(__name__)


CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})

app.register_blueprint(user_router)
app.register_blueprint(class_router)
app.register_blueprint(subject_router)
app.register_blueprint(auth_router)
app.register_blueprint(grade_router)


@app.errorhandler(500)
def internal_error(e):
    """Handled resource internal server error."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(401)
def unathorized_error(e):
    """Handled resource unauthorized error."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(403)
def unathorized_access(e):
    """Handled resource unauthorized error."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.teardown_appcontext
def close_session(exception=None):
    """Close current session."""
    storage.close_session()


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
