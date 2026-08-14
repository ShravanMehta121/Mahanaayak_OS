import re
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.services.activity_logger import ActivityLogger

class UserService:
    @staticmethod
    def validate_password(password):
        # Requires 8+ chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        return bool(regex.match(password))

    @staticmethod
    def create_user(data, current_user_id=None):
        if User.query.filter_by(username=data.get('username')).first():
            return None, "Username already exists"
        if User.query.filter_by(email=data.get('email')).first():
            return None, "Email already exists"
        if data.get('phone') and User.query.filter_by(phone=data.get('phone')).first():
            return None, "Phone number already exists"
        
        password = data.get('password')
        if not password or not UserService.validate_password(password):
            return None, "Password does not meet strong password requirements"
        
        role = Role.query.filter_by(name=data.get('role')).first()
        if not role:
            return None, "Invalid role"
        
        user = User(
            name=data.get('name'),
            username=data.get('username'),
            email=data.get('email'),
            phone=data.get('phone'),
            password_hash=generate_password_hash(password),
            role_id=role.id,
            assigned_ward_id=data.get('assigned_ward_id'),
            assigned_department_id=data.get('assigned_department_id'),
            is_active=data.get('is_active', True)
        )
        db.session.add(user)
        db.session.commit()
        
        ActivityLogger.log("USER_CREATED", f"Created user {user.username}", current_user_id)
        return user, None

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id, data, current_user_id=None):
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        
        # Unique constraints checks
        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                return None, "Username already exists"
            user.username = data['username']
            
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return None, "Email already exists"
            user.email = data['email']
            
        if 'phone' in data and data['phone'] != user.phone:
            if User.query.filter_by(phone=data['phone']).first():
                return None, "Phone number already exists"
            user.phone = data['phone']

        if 'name' in data:
            user.name = data['name']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'assigned_ward_id' in data:
            user.assigned_ward_id = data['assigned_ward_id']
        if 'assigned_department_id' in data:
            user.assigned_department_id = data['assigned_department_id']
        
        if 'role' in data:
            role = Role.query.filter_by(name=data['role']).first()
            if not role:
                return None, "Invalid role"
            user.role_id = role.id
            
        if 'password' in data and data['password']:
            if not UserService.validate_password(data['password']):
                return None, "Password does not meet strong password requirements"
            user.password_hash = generate_password_hash(data['password'])

        db.session.commit()
        ActivityLogger.log("USER_UPDATED", f"Updated user {user.username}", current_user_id)
        return user, None

    @staticmethod
    def delete_user(user_id, current_user_id=None):
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        
        db.session.delete(user)
        db.session.commit()
        ActivityLogger.log("USER_DELETED", f"Deleted user {user.username}", current_user_id)
        return True, None
