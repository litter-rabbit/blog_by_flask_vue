
from flask import jsonify

from app.api import api_bp

@api_bp.route('/ping',methods=['GET'])
def ping():

    return jsonify('Pong')
