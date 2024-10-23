from .app import *
from flask import render_template, url_for, redirect, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField, DecimalField, SelectField, RadioField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from flask_login import login_required
from app.models import *
from sqlalchemy import func
from io import BytesIO
from fpdf import FPDF


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
    # type = QuerySelectField("Type de déchet", query_factory=get_categories, allow_blank=True, get_label="Nom_Type")
    quantite = DecimalField("Volume du déchet", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

@app.route("/insert-dechets", methods=["GET", "POST"])
# @login_required
def insert_dechets():
    form = DechetsForm()
    if form.validate_on_submit():
        insert_dechet(form.nom.data, form.type.data, form.quantite.data)
        return redirect(url_for("home"))
    return render_template("insertion_dechets.html", form=form)

@app.route("/rapport")
def rapport():
    traiter = get_traiter_by_date()
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
        pdf.cell(40, 10, str(traiter[0]), 1)  # id_point_collecte
        pdf.cell(40, 10, str(traiter[1]), 1)  # id_Type
        pdf.cell(40, 10, str(traiter[2]), 1)  # dateCollecte
        pdf.cell(40, 10, str(traiter[3]), 1)  # qtecollecte
        pdf.ln()

    # Sauvegarder le PDF dans un buffer en mémoire
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    # Envoyer le fichier PDF au client
    return send_file(pdf_output, attachment_filename=f"rapport_{date_collecte}.pdf", as_attachment=True)

