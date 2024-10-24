from .app import *
from flask import render_template, url_for, redirect, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField, DecimalField, SelectField, RadioField,PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Email,Length,Regexp
from flask_login import login_required
from app.models import *
from sqlalchemy import func
from io import BytesIO
from fpdf import FPDF

class UtilisateurForm(FlaskForm):
    nom_utilisateur = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=1, max=25)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    numtel = StringField("Numéro de téléphone", validators=[DataRequired(), Length(max=15), Regexp(r'^\d+$', message="Le numéro de téléphone doit contenir uniquement des chiffres.")])
    motdepasse = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6, max=35)])
    entreprise = SelectField("Entreprise", choices=get_entreprise, validators=[DataRequired()])
    submit = SubmitField("Ajouter")
@app.route("/")
def home():

    if 'nom_Utilisateur' in session:
        return render_template("home.html",username=session['nom_Utilisateur'])
    else:
        return render_template("home.html")

class LoginForm(FlaskForm):
    nom_utilisateur = StringField("Nom d'utilisateur", validators=[DataRequired()])
    motdepasse = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = get_nom_utilisateur(form.nom_utilisateur.data)
        mdp_entre = form.motdepasse.data
        if existing_user and mdp_entre == get_motdepasse(existing_user[0]):
            # Si l'utilisateur existe et que le mot de passe est correct
            session['nom_Utilisateur'] = form.nom_utilisateur.data
            return redirect(url_for('home'))
        else:
            # Mot de passe ou nom d'utilisateur incorrect
            return render_template('login.html', error="Nom d'utilisateur ou mot de passe incorrect", form=form)
    
    # Si la méthode est GET, on retourne le formulaire de connexion
    return render_template('login.html', form=form)

   

       


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UtilisateurForm()
    if form.validate_on_submit():
        existing_user = get_nom_utilisateur(form.nom_utilisateur.data)
        if existing_user:
            # Si l'utilisateur existe déjà, retourner un message d'erreur
            return render_template('register.html', error="Le nom d'utilisateur est déjà pris", form=form)

        # Insertion dans la base de données
        insert_user(form.nom_utilisateur.data, form.email.data, form.numtel.data, form.motdepasse.data, form.entreprise.data, "utilisateur")
        # Rediriger vers la page d'accueil après inscription réussie
        session['nom_Utilisateur'] = form.nom_utilisateur.data
        return redirect(url_for('home'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('nom_Utilisateur', None)
    return redirect(url_for('home'))

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
@app.route("/rapport")
def rapport():
    traiter = get_traiter_sort_by_date()
    return render_template("rapport.html", traiter=traiter[:10])


@app.route('/download_pdf/<date_collecte>')
def download_pdf(date_collecte):
    # Récupérer les données pour cette date
    traiter_list = get_traiter_by_date(date_collecte)

    if not traiter_list:
        return "Aucune collecte trouvée pour cette date."

    # Créer un PDF avec les données récupérées
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)

    # Titre du PDF
    pdf.cell(200, 10, f"Rapport de collecte pour le {date_collecte}", ln=True, align='C')

    # Ajouter les en-têtes de table
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, 'Point de Collecte', 1)
    pdf.cell(40, 10, 'Type de Dechet', 1)
    pdf.cell(40, 10, 'Date Collecte', 1)
    pdf.cell(40, 10, 'Quantité Collectée (kg)', 1)
    pdf.ln()

    # Ajouter les données dans le PDF
    pdf.set_font('Arial', '', 10)
    for traiter in traiter_list:
        pdf.cell(40, 10, str(traiter.id_point_collecte), 1)  # id_point_collecte
        pdf.cell(40, 10, str(traiter.id_Type), 1)  # id_Type
        pdf.cell(40, 10, str(traiter.dateCollecte), 1)  # dateCollecte
        pdf.cell(40, 10, str(traiter.qtecollecte), 1)  # qtecollecte
        pdf.ln()

    # Sauvegarder le PDF dans un buffer en mémoire
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)

    # Envoyer le fichier PDF au client
    return send_file(pdf_output, download_name=f"rapport_{date_collecte}.pdf", as_attachment=True)

