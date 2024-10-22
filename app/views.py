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