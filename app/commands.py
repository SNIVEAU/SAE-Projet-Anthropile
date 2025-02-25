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

    