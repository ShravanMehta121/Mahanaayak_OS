from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.constants.roles import UserRole
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Ensure roles exist
    admin_role = Role.query.filter_by(name=UserRole.ADMIN.value).first()
    member_role = Role.query.filter_by(name=UserRole.TEAM_MEMBER.value).first()
    
    if not admin_role:
        admin_role = Role(name=UserRole.ADMIN.value, description="Admin role")
        db.session.add(admin_role)
    if not member_role:
        member_role = Role(name=UserRole.TEAM_MEMBER.value, description="Member role")
        db.session.add(member_role)
    db.session.commit()

    # Fix Admin
    admin = User.query.filter_by(username="admin").first()
    if admin:
        admin.password_hash = generate_password_hash("admin123")
    else:
        admin = User(
            name="System Admin",
            username="admin",
            email="admin@mahanaayakos.com",
            phone="1234567890",
            password_hash=generate_password_hash("admin123"),
            role_id=admin_role.id
        )
        db.session.add(admin)

    # Fix Office
    office = User.query.filter_by(username="office").first()
    if office:
        office.password_hash = generate_password_hash("office123")
    else:
        office = User(
            name="Office Member",
            username="office",
            email="office@mahanaayakos.com",
            phone="0987654321",
            password_hash=generate_password_hash("office123"),
            role_id=member_role.id
        )
        db.session.add(office)

    db.session.commit()
    print("Users admin and office have been successfully configured.")
