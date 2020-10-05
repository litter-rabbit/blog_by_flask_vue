
from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify
from app.api import api_bp
from app import db
def error_response(status_code,message=None):
    pyload={'status_code':HTTP_STATUS_CODES.get(status_code,'Unknow error')}
    if message:
        pyload['message']=message
    response=jsonify(pyload)
    response.status_code=status_code
    return response

def bad_request(message):
    return error_response(400,message)


@api_bp.app_errorhandler(500)
def internal_error(erros):
    db.session.rollback()
    return error_response(500)

@api_bp.app_errorhandler(404)
def not_found_error(erros):
    return error_response(404)




    
