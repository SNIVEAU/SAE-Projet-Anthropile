from .app import *
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField, DecimalField, SelectField, RadioField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from flask_login import login_required
from app.models import *
from sqlalchemy import func


@app.route("/")
def home():

    if 'nom_Utilisateur' in session:
        return render_template("home.html",username=session['nom_Utilisateur'])
    else:
        return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['nom_Utilisateur']
        print(username)
        pwd = request.form['motdepasse']
        cur = mysql.connection.cursor()
        cur.execute("SELECT nom_Utilisateur, motdepasse FROM UTILISATEUR WHERE nom_Utilisateur = %s", [username])
        user = cur.fetchone()
        cur.close()

        if user and pwd == user[1]:
            session['nom_Utilisateur'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password') 

    return render_template('login.html')
       


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom_utilisateur = request.form['nom_Utilisateur']
        mail = request.form['mail']
        numtel = request.form['numtel']
        motdepasse = request.form['motdepasse']
        id_entreprise = request.form['id_Entreprise']
        
        # Vérifier si l'utilisateur existe déjà
        cur = mysql.connection.cursor()
        cur.execute("SELECT nom_Utilisateur FROM UTILISATEUR WHERE nom_Utilisateur = %s", [nom_utilisateur])
        existing_user = cur.fetchone()
        
        if existing_user:
            # Si l'utilisateur existe déjà, retourner un message d'erreur
            cur.close()
            return render_template('register.html', error="Le nom d'utilisateur est déjà pris")
       
        # Insertion dans la base de données
        cur.execute("INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel, motdepasse, id_Entreprise) VALUES (%s, %s, %s, %s, %s)", 
                    (nom_utilisateur, mail, numtel, motdepasse, id_entreprise))
        mysql.connection.commit()
        cur.close()
        
        # Enregistrer l'utilisateur dans la session après l'inscription
        session['nom_Utilisateur'] = nom_utilisateur
        
        # Rediriger vers la page d'accueil après inscription réussie
        return redirect(url_for('home'))
    
    # Si la méthode est GET, afficher la page d'inscription
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('nom_Utilisateur', None)
    return redirect(url_for('home'))


    return render_template("home.html",)

class DechetsForm(FlaskForm):
    # id_dechet = HiddenField("ID du déchet")
    nom = StringField("Nom du déchet", validators=[DataRequired()])
    # type = StringField("Type de déchet", validators=[DataRequired()])
    # type = SelectField("Type de déchet", choices=[("plastique", "Plastique"), ("verre", "Verre"), ("papier", "Papier"), ("métal", "Métal"), ("organique", "Organique")], validators=[DataRequired()])
    type = SelectField("Type de déchet", choices=get_categories, validators=[DataRequired()])
    # type = RadioField("Type de déchet", choices=get_categories)
    # type = QuerySelectField("Type de déchet", query_factory=get_categories, allow_blank=False, get_label="Nom_Type", validators=[DataRequired()])
    quantite = DecimalField("Volume du déchet", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

@app.route("/insert-dechets", methods=["GET", "POST"])
# @login_required
def insert_dechets():
    form = DechetsForm()
    if form.validate_on_submit():
        print(type(form.type.data))
        dechet = Dechet(form.nom.data, form.type.data, form.quantite.data)
        dechet.insert_dechet()
        # insert_dechet(form.nom.data, form.type.data, form.quantite.data)
        return redirect(url_for("home"))
    return render_template("insertion_dechets.html", form=form)

@app.route("/collecte-dechets")
def collecte_dechets():
    return render_template("collecte_dechets.html", points_de_collecte=get_points_de_collecte())