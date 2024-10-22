from .app import *
from flask import render_template, url_for, redirect
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

