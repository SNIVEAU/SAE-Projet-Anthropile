import click
from .app import app, mysql

@app.cli.command()
@click.argument('username')
def toadmin(username):
    """
    Change role to admin.
    """
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE UTILISATEUR SET nom_role = 'Administrateur' WHERE nom_Utilisateur = %s", (username,))
        mysql.connection.commit()
        cursor.close()
        print(f"L'utilisateur {username} a été promu au rôle Administrateur.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
