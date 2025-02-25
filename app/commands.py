import click
from app.models import *

from flask import Flask
from werkzeug.security import generate_password_hash
import click

@app.cli.command("create-admin")
@click.argument("username")
@click.argument("email")
@click.argument("phone")
@click.argument("password")
def create_admin(username, email, phone, password):
    """Crée un administrateur via la ligne de commande"""
    
    # Vérifier si l'utilisateur existe déjà
    existing_user = get_nom_utilisateur(username)
    if existing_user:
        click.echo("❌ Erreur : Ce nom d'utilisateur est déjà pris.")
        return
    
    # Hacher le mot de passe
    hashed_password = generate_password_hash(password)
    
    # Insérer l'utilisateur avec le rôle Admin
    insert_user(username, email, phone, hashed_password, "Administrateur")
    
    # Vérifier si l'utilisateur a bien été inséré
    admin_user = get_nom_utilisateur(username)
    if admin_user:
        click.echo(f"✅ Administrateur '{username}' créé avec succès !")
    else:
        click.echo("❌ Erreur lors de la création de l'administrateur.")

    

from .app import app, mysql
#cette ligne me parait bizarre car perso j'avais une erreur quand j'essayais d'importer app
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
def loaddb():
    '''Creates the tables and populates them with data.'''
    try:
        path = '../model/'
        files = ['creation.sql', 'insert.sql']
        cursor = mysql.connection.cursor()
        for file in files:
            with open(path + file, 'r', encoding="utf-8") as f:
                sql = f.read()
                for statement in sql.split(';'): 
                    if statement.strip():
                        if statement[0:2] != '--':
                            cursor.execute(statement)
        mysql.connection.commit()
        cursor.close()
        print("Les tables ont été créées et les données ont été insérées. \nLes triggers sont a ajouter manuellement.")
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

