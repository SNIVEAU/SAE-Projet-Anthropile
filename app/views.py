from functools import wraps
from .app import *
from flask import render_template, url_for, redirect, send_file, request, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, IntegerField, SubmitField, HiddenField, DecimalField, SelectField, RadioField,PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Email,Length,Regexp
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import current_user, login_required, login_user, logout_user
from app.models import *
from sqlalchemy import func
from io import BytesIO
from fpdf import FPDF
import requests
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
from geopy.exc import GeocoderUnavailable

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


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.nom_role != 'Administrateur':
            return redirect(url_for('not_admin'))
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
               
                login_user(user)  # Utilise l'option remember de Flask-Login
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
        existing_point = get_nom_pts_collecte(form.nom_utilisateur.data)
        if existing_user:
            # Si l'utilisateur existe déjà, retourner un message d'erreur
            return render_template('register.html', error="Le nom d'utilisateur est déjà pris", form=form)
        if existing_point:
            # Si le point de collecte existe déjà, retourner un message d'erreur
            return render_template('register.html', error="Un point de collecte existe déjà à cet endroit", form=form)
        try:
            pos = get_pos_irl(form.adresse.data)
            print(pos)
            if pos is None:
                return render_template('register.html', error="Adresse non trouvée", form=form)
            if 'Geocoder' in str(pos):
                return render_template('register.html', error="Service de géocodage indisponible", form=form)            
        except Exception as e:
            print(e, "-------------------")
            return render_template('register.html', error="Adresse non trouvée", form=form)
        # Hacher le mot de passe avant de l'insérer dans la base de données
        hashed_password = generate_password_hash(form.motdepasse.data)
        print("c'est le mot de passe hashed, longeur")
        # Insertion dans la base de données avec le mot de passe haché
        print(form.entreprise.data)
        insert_user(form.nom_utilisateur.data, form.email.data, form.numtel.data, hashed_password, "Utilisateur")
        if not form.entreprise.data == 'Aucune':
            idUtilisateur = get_id_utilisateur(form.nom_utilisateur.data)
            insert_travailler(idUtilisateur, form.entreprise.data)
        # or ('Geocoder' in str(pos) or 'Max retries' in str(pos) or '443' in str(pos) or 'timeout' in str(pos))
        try:
            if not isinstance(pos, GeocoderUnavailable):
                if not get_pts_de_collecte_by_adresse(form.adresse.data):
                    insert_pts_de_collecte(form.adresse.data, form.nom_utilisateur.data, 50, pos[0],pos[1])
                    ajoute_pts_de_collecte_specifique(get_max_id_pts_de_collecte(),get_max_id_user())
            else:
                flash("Votre adresse n'est pas défini comme un point de collecte", "warning")
        except Exception as e:
            print(e)
            flash("Votre adresse n'est pas défini comme un point de collecte", "warning")
        #récupérer l'inscrit dans la bd
        new_user = get_all_user_info(form.nom_utilisateur.data)
        if new_user:
            user_data = Utilisateur(*new_user)
            login_user(user_data)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()  # Déconnexion avec Flask-Login
    # Optionnellement, supprimer le cookie "remember_me" ici
    resp = redirect(url_for('home'))
    #resp.delete_cookie('remember_me')
    return resp

@app.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    return jsonify(is_logged_in=current_user.is_authenticated)
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
    id_point_collecte = SelectField("Point de collecte", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

@app.route("/insert-dechets", methods=["GET", "POST"])
@login_required
def insert_dechets():
    form = DechetsForm()

    user_points_de_collecte = get_points_de_collecte_by_user(current_user.id)
    print(user_points_de_collecte)
    form.id_point_collecte.choices = [(str(point.id_point_de_collecte), point.nom_pt_collecte) for point in user_points_de_collecte]

    if form.validate_on_submit():
        print(form.id_user.data, "''''''''''''''''''''")
        print(form.id_point_collecte.data, "-----------------")
        print(type(form.id_point_collecte.data))

        print(est_possable(form.id_point_collecte.data, form.quantite.data))
        if not est_possable(form.id_point_collecte.data, form.quantite.data):
            espace_restant = get_espace_restant(form.id_point_collecte.data)
            flash("La quantité de déchet dépasse la capacité maximale du point de collecte. \nL'espace restant dans ce point de collecte est de " + str(espace_restant) + "kg. ", "error")
            return redirect(url_for("insert_dechets"))
        dechet = Dechet(form.nom.data, form.type.data, form.quantite.data)
        id_dechet = dechet.insert_dechet()
        
        result = insert_dechet_utilisateur(id_dechet, current_user.id, int(form.id_point_collecte.data))
        if result is None:
            flash("Déchet ajouté avec succès", "success")
            return redirect(url_for("insert_dechets"))
        else:
            flash(str(result), "error")
            return redirect(url_for("insert_dechets"))

    return render_template(
        "insertion_dechets.html",
        form=form,
        points_de_collecte=user_points_de_collecte,
    )

@app.route("/collecte-dechets")
# @login_required
def collecte_dechets():
    return render_template("collecte_dechets.html", points_de_collecte=get_points_de_collecte())

# @app.route("/statistique-dechets")
# @login_required
# def statistique_dechet():
#     # get_graph_dechet()
#     # get_graph_qte_dechets_categorie()
#     # data_graph_qte_dechets_categorie()
#     # return render_template("statistique_dechet.html", points_de_collecte=get_points_de_collecte())
#     return render_template("statistique_dechet.html", points_de_collecte=get_points_de_collecte())

@app.route("/data/dechets")
# @login_required
def statistique_dechets():
    return data_graph_qte_dechets_categorie()

@app.route("/statistique-pts-collecte")
@login_required
def statistique_pts_collecte():
    return render_template("statistique_pts_collecte.html", points_de_collecte=get_points_de_collecte(),pts_remplis=get_pts_remplis())

@app.route("/data/graph-pts-collecte")
# @login_required
def data_graph_pts_collecte():
    return data_graph_qte_dechets_cat_pts_collecte()

@app.route("/rapport")
@login_required
def rapport():
    collecter = get_collecter_sort_by_date()
    collecter = remove_doublon_date_collecter(collecter)
    return render_template("rapport.html", collecter=collecter[:10])


@app.route('/download_pdf/<date_collecte>')
@login_required
def download_pdf(date_collecte):
    # Récupérer les données pour cette date
    collecter_list = get_collecter_by_date(date_collecte)

    if not collecter_list:
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
    for collecter in collecter_list:
        pdf.cell(40, 10, str(collecter.id_point_collecte), 1)  # id_point_collecte
        pdf.cell(40, 10, str(collecter.id_Type), 1)  # id_Type
        pdf.cell(40, 10, str(collecter.dateCollecte), 1)  # dateCollecte
        pdf.cell(40, 10, str(collecter.qtecollecte), 1)  # qtecollecte
        pdf.ln()

    # Sauvegarder le PDF dans un buffer en mémoire
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)

    # Envoyer le fichier PDF au client
    return send_file(pdf_output, download_name=f"rapport_{date_collecte}.pdf", as_attachment=True)

@app.route("/details/<id>")
#@login_required
def detaille(id):
    points_de_collecte = get_points_de_collecte()
    liste_collectes = get_liste_collectes(int(id))
    for pt in points_de_collecte:
        if pt.id_point_de_collecte == int(id):
            return render_template("detail_collecte.html", point = pt, quantite_courant = get_quantite_courante(int(id)), collectes=liste_collectes)
    return render_template("collecte_dechets.html", points_de_collecte=get_points_de_collecte())

class PtsDeCollecteForm(FlaskForm):
    # id_dechet = HiddenField("ID du déchet")
    id_point_de_collecte = HiddenField("ID du point de collecte")
    latitude = DecimalField("Latitude")
    longitude = DecimalField("Longitude")
    adresse = StringField("Adresse du point de collecte", validators=[DataRequired()])
    nom_pt_collecte = StringField("Nom du point de collecte", validators=[DataRequired()])
    quantite_max = DecimalField("Quantité maximale de déchets", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

@app.route("/gerer-pts-collecte", methods=["GET", "POST"])
@login_required
@admin_required
def gerer_pts_collecte():
    form = PtsDeCollecteForm()
    if form.validate_on_submit():
        try:
            if adresse_existante_bd(form.adresse.data):
                print("Un point de collecte avec cette adresse existe déjà")
                return render_template("gerer_pts_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Un point de collecte avec cette adresse existe déjà")
            if nom_pt_collecte_existante_bd(form.adresse.data):
                print("Un point de collecte avec ce nom existe déjà")
                return render_template("gerer_pts_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Un point de collecte avec ce nom existe déjà")
            if form.latitude.data == None or form.longitude.data == None:
                pos = get_pos_irl(form.adresse.data)
            else:
                pos = (form.latitude.data, form.longitude.data)
            if pos is None:
                print("Adresse non trouvée")
                return render_template("gerer_pts_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Adresse non trouvée")
            insert_pts_de_collecte(
                form.adresse.data,
                form.nom_pt_collecte.data,
                form.quantite_max.data, 
                pos[0], pos[1]
            )
        except Exception as e:
            if 'Geocoder' in str(e):
                return render_template("gerer_pts_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Une erreur s'est produite lors de la recherche de l'adresse, veuillez réessayer plus tard")
            print(e)
            return render_template("gerer_pts_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Un point de collecte avec ce nom existe déjà")
        print("Point de collecte ajouté avec succès")
        return render_template("gerer_pts_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), success="Point de collecte ajouté avec succès")
    return render_template("gerer_pts_collecte.html", form=form, points_de_collecte=get_points_de_collecte())


@app.route("/modifier-pt-collecte/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def modifier_pt_collecte(id):
    form = PtsDeCollecteForm()
    point_de_collecte = get_point_collecte(id)
    current_pts = point_de_collecte
    if request.method == "GET":
        # Pré-remplir le formulaire avec les données existantes
        form.id_point_de_collecte.data = point_de_collecte.id_point_de_collecte
        form.adresse.data = point_de_collecte.adresse
        form.nom_pt_collecte.data = point_de_collecte.nom_pt_collecte
        form.quantite_max.data = point_de_collecte.quantite_max
    if form.validate_on_submit():
        # Mettre à jour le point de collecte
        adresse_existante = adresse_existante_bd(form.adresse.data)
        nom_existante = nom_pt_collecte_existante_bd(form.nom_pt_collecte.data)
        if adresse_existante and adresse_existante.id_point_de_collecte != id:
            return render_template("modifier_pt_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Un point de collecte avec cette adresse existe déjà")
        if nom_existante and nom_existante.id_point_de_collecte != id:
            print("Un point de collecte avec ce nom existe déjà")
            return render_template("modifier_pt_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Un point de collecte avec ce nom existe déjà")
        try:
            if form.adresse.data == current_pts.adresse and form.nom_pt_collecte.data == current_pts.nom_pt_collecte and form.quantite_max.data == current_pts.quantite_max:
                print("Aucune modification apportée")
                flash("Aucune modification apportée", "success")
                return redirect(url_for("gerer_pts_collecte"))
                # return render_template("modifier_pt_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Aucune modification apportée")
            fait = update_point_collecte(
                id,
                form.adresse.data,
                form.nom_pt_collecte.data,
                form.quantite_max.data
            )
            if fait is None:
                print("Adresse non trouvée")
                return render_template("modifier_pt_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Adresse non trouvée")
            if 'Geocoder' in str(fait):
                print("Une erreur s'est produite lors de la recherche de l'adresse, veuillez réessayer plus tard")
                return render_template("modifier_pt_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Une erreur s'est produite lors de la recherche de l'adresse, veuillez réessayer plus tard")
            flash("Point de collecte modifié avec succès", "success")            

            return redirect(url_for("gerer_pts_collecte"))
        except Exception as e:
            print(e)
            return render_template("modifier_pt_collecte.html", form=form, points_de_collecte=get_points_de_collecte(), error="Adresse non trouvée")
    return render_template("modifier_pt_collecte.html", form=form, points_de_collecte=get_points_de_collecte())

@app.route("/supprimer-pt-collecte/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def supprimer_pt_collecte(id):
    try:
        delete_pts_collecte_Appartenir(id)
        delete_point_collecte(id)
        flash("Point de collecte supprimé avec succès", "success")
        return redirect(url_for("gerer_pts_collecte"))
    except Exception as e:
        print(e)
        flash("Impossible de supprimer ce point de collecte, il y a des collectes et/ou déchets associées à ce point de collecte", "error")
        return redirect(url_for("gerer_pts_collecte"))

@app.route("/entreprises/")
@login_required
@admin_required
def toutes_entreprises():
    return render_template(
        "all_companies.html",
        entreprises=get_entreprise_sous_forme_classe()
    )

@app.route("/supprimer_entreprise/<int:id>")
@login_required
@admin_required
def supprimer_entreprise(id):
    if delete_company(int(id)):
        return redirect(url_for('toutes_entreprises', status='delete_success'))
    else:
        return redirect(url_for('toutes_entreprises', status='delete_error'))


@app.route("/modifier_entreprise/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
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

@app.route("/inserer_ent", methods=['GET', 'POST'])
@login_required
@admin_required
def inserer_entreprise():
    if request.method == "POST":
        id_ent = get_id_max_entreprise() + 1

        nom_entreprise = request.form.get("nom_entreprise")
        
        # Call insert_entreprise only once and store the result
        success = insert_entreprise(id_ent, nom_entreprise)
        
        if success:
            return redirect(url_for('toutes_entreprises', status='insert_success'))
        else:
            return redirect(url_for('inserer_entreprise', status='insert_error'))
    
    return render_template("insert_company.html", id_entreprise = get_id_max_entreprise() + 1)

class EditProfileForm(FlaskForm):
    user_id = HiddenField("User ID")  # Champ caché pour l'ID de l'utilisateur
    nom_utilisateur = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=20)])
    mail = StringField("Email", validators=[DataRequired(), Email()])
    numtel = StringField("Numéro de téléphone", validators=[DataRequired(), Length(min=10, max=15)])
    motdepasse = PasswordField("Mot de passe", validators=[Optional(), Length(min=8)])
    nom_role = SelectField("Rôle", choices=[("user", "Utilisateur"), ("admin", "Administrateur")])
    submit = SubmitField("Sauvegarder les modifications")

@app.route("/profil")
@login_required
def profil():
    return render_template("profil.html", user=current_user)

@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()

    if request.method == "GET":
        form.user_id.data = current_user.id  # Remplit le champ caché avec l'ID de l'utilisateur
        form.nom_utilisateur.data = current_user.nom_utilisateur
        form.mail.data = current_user.mail
        form.numtel.data = current_user.numtel
        form.nom_role.data = current_user.nom_role  # Charge le rôle actuel pour l'afficher

    if request.method == "POST":
        user_id = form.user_id.data  
        nom_utilisateur = form.nom_utilisateur.data
        mail = form.mail.data
        numtel = form.numtel.data
        
        if not update_user(user_id, nom_utilisateur, mail, numtel):
            return render_template("edit_profile.html", form=form, error="Une erreur s'est produite lors de la modification de l'utilisateur")

        current_user.nom_utilisateur = nom_utilisateur
        current_user.mail = mail
        current_user.numtel = numtel
        if form.motdepasse.data:
            current_user.password = form.motdepasse.data
            hashed_password = generate_password_hash(form.motdepasse.data)

            update_password(user_id,hashed_password)

        return redirect(url_for('profil'))

    return render_template("edit_profile.html", form=form, error="")


from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FieldList, FormField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, NumberRange

class PlanificationTournéeForm(FlaskForm):
    categorie = SelectField('Catégorie de déchet', coerce=int, validators=[DataRequired()])
    quantite = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=0)])
    date_collecte = DateField('Date de collecte', validators=[DataRequired()])
    heure_collecte = TimeField('Heure de collecte', validators=[DataRequired()])
    duree = IntegerField('Durée de la tournée', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Valider')
    
@app.route('/planification_tournee', methods=['GET', 'POST'])
@login_required
@admin_required
def planification_tournee():
    pts_de_collecte = get_points_de_collecte()
    categories_dechet = get_categories()
    form = PlanificationTournéeForm()
    if request.method == 'POST':
        date_collecte = datetime.combine(form.date_collecte.data, form.heure_collecte.data)
        insert_tournee(date_collecte, form.duree.data)
        id_tournee = get_last_tournee()
        for point in pts_de_collecte:
            categorie_id = request.form.get(f'categorie_{point.id_point_de_collecte}')
            if categorie_id:
                qte_collecte = get_qte_by_pts_and_type(point.id_point_de_collecte, categorie_id)
                print(f"Point de collecte: {point.nom_pt_collecte}, Catégorie: {categorie_id}")        
                insert_collecter(point.id_point_de_collecte, id_tournee,categorie_id, qte_collecte,) 
        return redirect(url_for('home'))

    return render_template(
        'planification_tournee.html',
        form=form,
        points_de_collecte=pts_de_collecte,
        categories_dechet=categories_dechet
    )
  
@app.route("/not_admin")
def not_admin():
    return render_template("not_admin.html")

@app.route("/categories/")
@login_required
def toutes_categories():
    print(get_categories())
    return render_template(
        "all_categories.html",
        categories=get_categories()
    )

@app.route("/inserer_categorie", methods=['GET', 'POST'])
@login_required
def inserer_categorie_dechet():
    if request.method == "POST":
        id_type = get_id_max_dechets() + 1

        nom_type = request.form.get("nom_type")
        priorite = request.form.get("priorite")
        
        # Call insert_entreprise only once and store the result
        success = insert_categorie(id_type, nom_type, priorite)
        
        if success:
            return redirect(url_for('toutes_categories', status='insert_success'))
        else:
            return redirect(url_for('inserer_categorie_dechet', status='insert_error'))
    
    return render_template("insert_category.html", id_categorie_max = get_id_max_dechets() + 1)

@app.route("/supprimer_categorie/<int:id>")
@login_required
def supprimer_cat(id):
    if delete_category(id):
        return redirect(url_for('toutes_categories', status='delete_success'))
    else:
        return redirect(url_for('toutes_categories', status='delete_error'))

@app.route("/avis")
def avis():
    return render_template("avis.html", avis=get_avis(), note_globale=get_global_note())

@app.route("/inserer_avis", methods=['GET', 'POST'])
@login_required
def add_avis():
    avis_text = request.form.get("avis")
    note = request.form.get("note")
    if note is None:
        note = 5
    if avis_text:
        insert_avis(current_user.id , avis_text, note)
        flash("Avis ajouté avec succès", "success")
    else:
        flash("Votre avis ne peut pas être vide.", "error")

    return redirect(url_for('avis'))


@app.route('/delete_avis/<int:avis_id>', methods=['POST', 'GET'])
def delete_avis(avis_id):
    if not current_user.is_admin():
        flash("Vous devez être administrateur pour supprimer un avis.", "danger")
        return redirect(url_for('avis'))  # Remplace 'avis' par la page où les avis sont affichés
    if avis_id:
        delete_avis_id(avis_id)
        flash("Avis supprimé avec succès", "success")
    else:
        flash("Avis non trouvé.", "danger")
    
    return redirect(url_for('avis'))  # Redirige vers la page des avis

@app.route("/dechets_selon_utilisteur/<int:id>")
@login_required
def tous_dechets_selon_utilisateur(id):
    return render_template(
        "all_dechets.html",
        dechets=get_tous_dechets_selon_utilisateur(id),
        dechets_collectes = get_tous_dechets_collectes_selon_utilisateur(id)
    )

@app.route("/notifications")
@login_required
@admin_required
def notifications():
    return render_template('notifications.html', notifications=get_all_alertes())



@app.route('/marquer_lu/<int:notification_id>', methods=['POST'])
def marquer_lu(notification_id):
    try:
        mark_as_read(notification_id)
        flash("Notification marquée comme lue avec succès.", "success")

        return redirect(url_for('notifications'))
    except Exception as e:
        flash(f"Erreur lors de la mise à jour de la notification: {str(e)}", "danger")
        return redirect(url_for('notificatons'))


@app.context_processor
def inject_notifications_non_lues():
    alertes_non_lues = len(get_alertes_non_lues())
    return dict(notifications_non_lues=alertes_non_lues)


