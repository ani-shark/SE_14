from flask import Blueprint, request, jsonify
from flask.views import MethodView
from ai_agent.models import User,RoleEnum
from datetime import timedelta
from flask_jwt_extended import create_access_token,create_refresh_token,\
    set_access_cookies,set_refresh_cookies,jwt_required,unset_jwt_cookies,get_jwt_identity


auth_bp = Blueprint('auth', __name__)



class AuthAPI(MethodView):

    def post(self):
        data = request.get_json()
    
        user = User.query.filter_by(email = data.get('email')).first()
            
        if not user:
            return jsonify(error='invalid user credentials'),401
            
        response = jsonify(message="sign in successful.")
        if user.role == RoleEnum.ADMIN:
            access_token = create_access_token(identity=str(user.id),expires_delta=timedelta(minutes=35))
            refresh_token = create_refresh_token(identity=str(user.id),expires_delta=timedelta(minutes=180))  

            set_access_cookies(response,access_token,max_age=timedelta(minutes=30))
            set_refresh_cookies(response,refresh_token,max_age=timedelta(minutes=175))
        
        else:
            access_token = create_access_token(identity=str(user.id),expires_delta=timedelta(minutes=60))
            refresh_token = create_refresh_token(identity=str(user.id),expires_delta=timedelta(days=15))

            set_access_cookies(response,access_token,max_age=timedelta(minutes=55))
            set_refresh_cookies(response,refresh_token,max_age=timedelta(days=14))

        
        return response,200
    
    
    @jwt_required(verify_type=False)
    def delete(self):
        response = jsonify(message="signout successful.")
        unset_jwt_cookies(response)
        return response,200
        
  

class RefreshAPI(MethodView):
    
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user:
            response = jsonify(message="access token refreshed")

            if user.role == RoleEnum.ADMIN:
                access_token = create_access_token(identity=str(user.id),expires_delta=timedelta(minutes=35))
                set_access_cookies(response,access_token,max_age=timedelta(minutes=30))
            
            else:
                access_token = create_access_token(identity=str(user.id),expires_delta=timedelta(minutes=60))
                set_access_cookies(response,access_token,max_age=timedelta(minutes=55))

            
            return response,200

        else:
            return jsonify(error='invalid request.'),401


authenticate_view = AuthAPI.as_view('authenticate')
refresh_view = RefreshAPI.as_view('refresh')

auth_bp.add_url_rule('/signin', view_func=authenticate_view, methods=['POST'])
auth_bp.add_url_rule('/signout', view_func=authenticate_view, methods=['DELETE'])
auth_bp.add_url_rule('/refresh',view_func=refresh_view,methods = ['POST'])

