# import click
# from app import db
# from app.models import User

# @click.command('create-admin')
# @click.argument('username')
# @click.argument('email')
# @click.argument('password')
# def create_admin(username, email, password):
#     """Create a new admin user."""
#     admin_user = User(username=username, email=email, is_admin=True)
#     admin_user.set_password(password)
#     db.session.add(admin_user)
#     db.session.commit()
#     click.echo(f'Admin user {username} created successfully.')

# if __name__ == '__main__':
#     create_admin()