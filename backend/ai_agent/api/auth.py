from flask import Blueprint, request, jsonify
from flask.views import MethodView
from ai_agent.models import User,RoleEnum
from datetime import timedelta
from flask_jwt_extended import create_access_token,create_refresh_token,\
    set_access_cookies,set_refresh_cookies,jwt_required,unset_jwt_cookies,get_jwt_identity

from ai_agent.validation import validate_email


auth_bp = Blueprint('auth', __name__)



class AuthAPI(MethodView):
    def post(self):
        data = request.get_json()

        if not validate_email(data.get('email','')):
            return jsonify(error='invalid or missing email'), 400

        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return jsonify(error='invalid user credentials'), 401

        # ✅ Generate JWT tokens
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=60))
        refresh_token = create_refresh_token(identity=str(user.id), expires_delta=timedelta(days=15))

        # ✅ Include tokens in response JSON
        response_data = {
            "message": "sign in successful.",
            "id": user.id,
            "email": user.email,
            "role": user.role.value,
            "access_token": access_token,  
            "refresh_token": refresh_token 
        }

        response = jsonify(response_data)

        set_access_cookies(response, access_token, max_age=timedelta(minutes=55))
        set_refresh_cookies(response, refresh_token, max_age=timedelta(days=14))

        return response, 200
        
  

class RefreshAPI(MethodView):
    
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify(error='invalid request.'),401

        response = jsonify(message="access token refreshed")
        if user.role == RoleEnum.ADMIN:
          
            access_token = create_access_token(identity=str(user.id),expires_delta=timedelta(minutes=35))
            set_access_cookies(response,access_token,max_age=timedelta(minutes=30))
        else:
            
            access_token = create_access_token(identity=str(user.id),expires_delta=timedelta(minutes=60))
            set_access_cookies(response,access_token,max_age=timedelta(minutes=55))
        
        
        response = jsonify(
            message="sign in successful.", 
            role=user.role.value, 
            id=user.id,
            access_token=access_token  
        )

    


authenticate_view = AuthAPI.as_view('authenticate')
refresh_view = RefreshAPI.as_view('refresh')

auth_bp.add_url_rule('/signin', view_func=authenticate_view, methods=['POST'])
auth_bp.add_url_rule('/signout', view_func=authenticate_view, methods=['DELETE'])
auth_bp.add_url_rule('/refresh',view_func=refresh_view,methods = ['POST'])

