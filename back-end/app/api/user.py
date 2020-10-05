
from app.api import api_bp
from app.api.erros import bad_request
from flask import request,jsonify,url_for
from app.modles import User
from app import db
import re

@api_bp.route('/users',methods=['GET'])
def get_users():
    """返回所有用户"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)



@api_bp.route('/users',methods=['POST'])
def create_user():
    """注册一个用户"""
    data=request.get_json()

    if not data:
        return bad_request('you must post json data')
    
    message={}
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'Please provide a valid username.'

    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'
    if 'password' not in data or not data.get('password', None):
        message['password'] = 'Please provide a valid password.'

    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = 'Please use a different username.'
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = 'Please use a different email address.'
    if message:
        return bad_request(message)

    user = User()
    user.form_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response



@api_bp.route('/users/<int:id>',methods=['DELETE'])
def delete_user(id):
    """删除一个用户"""
    pass

@api_bp.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    """根据id返回用户"""

    return jsonify(User.query.get_or_404(id).to_dict())
   

@api_bp.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    """修改一个用户"""

    user=User.query.get_or_404(id)
    data=request.get_json()

    if not data:
        return bad_request('you have privode json')

    message={}
    if 'username' in data and not data.get('username', None):
        message['username'] = 'Please provide a valid username.'

    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' in data and not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'

    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        message['username'] = 'Please use a different username.'
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        message['email'] = 'Please use a different email address.'
    if message:
        return bad_request(message)

    user.form_dict(data, new_user=False)
    db.session.commit()
    response = jsonify(user.to_dict())
    return response
    




