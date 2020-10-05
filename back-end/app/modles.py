
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for


class PiginateAPIMinix(object):
    
    @staticmethod
    def to_collection_dict(query,page,per_page,endpoint,**kwargs):
        resource = query.paginate(page,per_page,False)
        data={
            'items':[item.to_dict() for item in resource.items ],
            '_meta':{
                'page':page,
                'per_page':per_page,
                'total_page':resource.pages,
                'total_items':resource.total
            },
            '_links':{
                'self':url_for(endpoint,page=page,per_page=per_page,**kwargs),
                'next':url_for(endpoint,page=page+1,per_page=per_page,**kwargs)if resource.has_next else None,
                'prev':url_for(endpoint,page=page-1,per_page=per_page,**kwargs)if resource.has_prev else None
            }

        }
        
        return data
    



class User(db.Model,PiginateAPIMinix):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User.{}>'.format(self.usrname)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password,password_hash):

        return check_password_hash(password_hash, password)
    
    def form_dict(self,data,new_user=False):
        for field in ['username','email']:
            if field in data:
                setattr(self,field,data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self,include_email=False):

        data={
            'id':self.id,
            'username':self.username,
            '_links':{
                'self':url_for('api.get_user',id=self.id)
            }
        }
        if include_email:
            data['emial']=self.email
        
        return data




