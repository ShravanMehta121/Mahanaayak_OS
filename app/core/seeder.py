import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models.role import Role
from app.models.user import User
from app.constants.roles import UserRole

@click.command("seed")
@with_appcontext
def seed_data():
    """Seed initial data like Roles and initial Admin/Member users."""
    
    # Seed Roles
    roles = [UserRole.ADMIN.value, UserRole.TEAM_MEMBER.value]
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name, description=f"{role_name} role"))
    
    db.session.commit()
    click.echo("Roles seeded.")
    
    # Seed Admin User
    admin_role = Role.query.filter_by(name=UserRole.ADMIN.value).first()
    if not User.query.filter_by(username="admin").first():
        admin = User(
            name="System Admin",
            username="admin",
            email="admin@mahanaayakos.com",
            phone="1234567890",
            password_hash=generate_password_hash("admin123"),
            role_id=admin_role.id
        )
        db.session.add(admin)
        click.echo("Admin user seeded.")

    # Seed Team Member
    member_role = Role.query.filter_by(name=UserRole.TEAM_MEMBER.value).first()
    if not User.query.filter_by(username="office").first():
        member = User(
            name="Office Member",
            username="office",
            email="office@mahanaayakos.com",
            phone="0987654321",
            password_hash=generate_password_hash("office123"),
            role_id=member_role.id
        )
        db.session.add(member)
        click.echo("Team Member seeded.")
        
    db.session.commit()
    click.echo("Seeding complete.")
