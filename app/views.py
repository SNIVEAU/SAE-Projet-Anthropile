from functools import wraps
from .app import *
from flask import render_template, url_for, redirect, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField, DecimalField, SelectField, RadioField,PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Email,Length,Regexp
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import current_user, login_required, login_user, logout_user
from app.models import *
from sqlalchemy import func
from io import BytesIO
from fpdf import FPDF

class UtilisateurForm(FlaskForm):
    nom_utilisateur = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=1, max=25)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    numtel = StringField("Numéro de téléphone", validators=[DataRequired(), Length(min = 10,max = 10), Regexp(r'^\d+$', message="Le numéro de téléphone doit contenir uniquement des chiffres.")])
    adresse = StringField("Adresse")
    motdepasse = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6, max=35)])
    entreprise = SelectField("Entreprise", choices=get_entreprise_register, validators=[DataRequired()])

    next = HiddenField()
    submit = SubmitField("Ajouter")


def guest(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    return render_template("home.html")


    #return decorated_function
class LoginForm(FlaskForm):
    nom_utilisateur = StringField("Nom d'utilisateur", validators=[DataRequired()])
    motdepasse = PasswordField("Mot de passe", validators=[DataRequired()])
    next = HiddenField()

    submit = SubmitField("Se connecter")
@app.route('/login', methods=['GET', 'POST'])
@guest
def login():
    form = LoginForm()
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    elif form.validate_on_submit():
        user_data = get_all_user_info(form.nom_utilisateur.data)
        
        if user_data:
            user = Utilisateur(*user_data)
            if check_password_hash(user.motdepasse, form.motdepasse.data):
                login_user(user)  # Connexion avec Flask-Login
                next = form.next.data or url_for("home")
                return redirect(next)
        
        return render_template('login.html', error="Nom d'utilisateur ou mot de passe incorrect", form=form)

    return render_template('login.html', form=form)

   

       


@app.route('/register', methods=['GET', 'POST'])
@guest
def register():
    form = UtilisateurForm()
    if form.validate_on_submit():
        existing_user = get_nom_utilisateur(form.nom_utilisateur.data)
        if existing_user:
            # Si l'utilisateur existe déjà, retourner un message d'erreur
            return render_template('register.html', error="Le nom d'utilisateur est déjà pris", form=form)

        # Hacher le mot de passe avant de l'insérer dans la base de données
        hashed_password = generate_password_hash(form.motdepasse.data)
        print("c'est le mot de passe hashed, longeur")
        # Insertion dans la base de données avec le mot de passe haché
        print(form.entreprise.data)
        insert_user(form.nom_utilisateur.data, form.email.data, form.numtel.data, hashed_password, "utilisateur")
        if not form.entreprise.data == 'Aucune':
            idUtilisateur = get_id_utilisateur(form.nom_utilisateur.data)
            insert_travailler(idUtilisateur, form.entreprise.data)
        if not get_pts_de_collecte_by_adresse(form.adresse.data):

            insert_pts_de_collecte(form.adresse.data, form.nom_utilisateur.data,0,0)

        #récupérer l'inscrit dans la bd
        new_user = get_all_user_info(form.nom_utilisateur.data)
        if new_user:
            user_data = Utilisateur(*new_user)
            login_user(user_data)

        return redirect(url_for('home'))
    
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required  # Protège cette route
def logout():
    logout_user()  # Déconnexion avec Flask-Login
    return redirect(url_for('home'))

class DechetsForm(FlaskForm):
    # id_dechet = HiddenField("ID du déchet")
    id_user = HiddenField("ID de l'utilisateur")
    nom = StringField("Nom du déchet", validators=[DataRequired()])
    # type = StringField("Type de déchet", validators=[DataRequired()])
    # type = SelectField("Type de déchet", choices=[("plastique", "Plastique"), ("verre", "Verre"), ("papier", "Papier"), ("métal", "Métal"), ("organique", "Organique")], validators=[DataRequired()])
    type = SelectField("Type de déchet", choices=get_categories, validators=[DataRequired()])
    # type = RadioField("Type de déchet", choices=get_categories)
    # type = QuerySelectField("Type de déchet", query_factory=get_categories, allow_blank=False, get_label="Nom_Type", validators=[DataRequired()])
    quantite = DecimalField("Volume du déchet", validators=[DataRequired()])
    id_point_collecte = SelectField("Point de collecte", choices=get_pts_collecte_and_id, validators=[DataRequired()])
    submit = SubmitField("Ajouter")

@app.route("/insert-dechets", methods=["GET", "POST"])
@login_required
def insert_dechets():
    form = DechetsForm()
    if form.validate_on_submit():
        print(form.id_user.data, "''''''''''''''''''''")
        print(form.id_point_collecte.data, "-----------------")
        print(form.id_point_collecte.data)
        print(type(form.id_point_collecte))
        dechet = Dechet(form.nom.data, form.type.data, form.quantite.data)
        id_dechet = dechet.insert_dechet()
        insert_dechet_utilisateur(id_dechet, current_user.id, int(form.id_point_collecte.data))
        # insert_dechet(form.nom.data, form.type.data, form.quantite.data)
        return redirect(url_for("home"))
    return render_template("insertion_dechets.html", form=form, points_de_collecte=get_points_de_collecte())

@app.route("/collecte-dechets")
@login_required
def collecte_dechets():
    return render_template("collecte_dechets.html", points_de_collecte=get_points_de_collecte())

@app.route("/statistique-dechets")
@login_required
def statistique_dechet():
    # get_graph_dechet()
    # get_graph_qte_dechets_categorie()
    # data_graph_qte_dechets_categorie()
    # return render_template("statistique_dechet.html", points_de_collecte=get_points_de_collecte())
    return render_template("statistique_dechet.html", points_de_collecte=get_points_de_collecte())

@app.route("/data/dechets")
@login_required
def statistique_dechets():
    return data_graph_qte_dechets_categorie()

@app.route("/statistique-pts-collecte")
@login_required
def statistique_pts_collecte():
    return render_template("statistique_pts_collecte.html", points_de_collecte=get_points_de_collecte())

@app.route("/data/graph-pts-collecte")
@login_required
def data_graph_pts_collecte():
    return data_graph_qte_dechets_cat_pts_collecte()

@app.route("/rapport")
@login_required
def rapport():
    traiter = get_traiter_sort_by_date()
    return render_template("rapport.html", traiter=traiter[:10])


@app.route('/download_pdf/<date_collecte>')
@login_required
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

@app.route("/details/<id>")
@login_required
def detaille(id):
    points_de_collecte = get_points_de_collecte()
    liste_collectes = get_liste_collectes(int(id))
    for pt in points_de_collecte:
        if pt.id_point_de_collecte == int(id):
            return render_template("detail_collecte.html", point = pt, quantite_courant = get_quantite_courante(int(id)), collectes=liste_collectes)
    return render_template("collecte_dechets.html", points_de_collecte=get_points_de_collecte())

@app.route("/entreprises/")
@login_required
def toutes_entreprises():
    return render_template(
        "all_companies.html",
        entreprises=get_entreprise_sous_forme_classe()
    )

@app.route("/supprimer_entreprise/<int:id>")
@login_required
def supprimer_entreprise(id):
    if delete_company(int(id)):
        return redirect(url_for('toutes_entreprises', status='delete_success'))
    else:
        return redirect(url_for('toutes_entreprises', status='delete_error'))


@app.route("/modifier_entreprise/<int:id>", methods=['GET', 'POST'])
@login_required
def modifier_entreprise(id):
    if request.method == "POST":
        nom_entreprise = request.form.get("nom_entreprise")
        success = update_entreprise(id, nom_entreprise)
        if success:
            return redirect(url_for('toutes_entreprises', status='modify_success'))
        else:
            return redirect(url_for('modifier_entreprise',id=id, status='modify_error'))
    return render_template(
        "edit_company.html", ent = get_entreprise_par_id(id)
    )  

@app.route("/inserer_entreprise", methods=['GET', 'POST'])
@login_required
def inserer_entreprise():
    if request.method == "POST":
        id_entreprise = get_id_max_entreprise() + 1

        nom_entreprise = request.form.get("nom_entreprise")
        
        # Call insert_entreprise only once and store the result
        success = insert_entreprise(id_entreprise, nom_entreprise)
        
        if success:
            return redirect(url_for('toutes_entreprises', status='insert_success'))
        else:
            return redirect(url_for('inserer_entreprise', status='insert_error'))
    
    return render_template("insert_company.html", id_entreprise = get_id_max_entreprise() + 1)
