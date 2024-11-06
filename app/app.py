from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

from flask_login import LoginManager, UserMixin
app = Flask(__name__)

app.secret_key = '3ade9a2f-84da-4b64-8b31-8fc35860d740'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#Mysql configuration
class Utilisateur(UserMixin):
    def __init__(self, id_Utilisateur, nom_Utilisateur, mail, numtel, motdepasse, nom_role):
        self.id = id_Utilisateur
        self.nom_utilisateur = nom_Utilisateur
        self.mail = mail
        self.numtel = numtel
        self.motdepasse = motdepasse
        self.nom_role = nom_role

@login_manager.user_loader
def load_user(user_name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM UTILISATEUR WHERE id_Utilisateur = %s", (user_name,))
    user_data = cursor.fetchone()
    cursor.close() #peut être remplacer par une fonction

    if user_data:
        return Utilisateur(*user_data)
    return None

app.config['MYSQL_HOST'] = 'servinfo-maria'
app.config['MYSQL_USER'] = 'lima'
app.config['MYSQL_PASSWORD'] = 'lima'
app.config['MYSQL_DB'] = 'DBlima' #mettre sa propre BD


mysql=MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)