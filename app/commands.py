import click
from .app import app, mysql
import re
import os

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

@app.cli.command()
def dropdb():
    '''Drops the tables.'''
    try:
        with open('../model/drop.sql', 'r', encoding="utf-8") as f:
            sql = f.read()
            cursor = mysql.connection.cursor()
            for statement in sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            mysql.connection.commit()
            cursor.close()
            print("Les tables ont été supprimées.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


