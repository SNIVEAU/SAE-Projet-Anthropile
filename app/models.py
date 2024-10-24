from .app import mysql

# def get_id_max_dechets():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT MAX(id_Dechet) FROM DECHET")
#     id_max,  = cursor.fetchone()
#     cursor.close()
#     print(id_max, "*********")
#     return id_max

def get_categories():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM CATEGORIEDECHET")
    categories = cursor.fetchall()
    cursor.close()
    print(categories)
    return categories

def get_id_type_dechet(nom_dechet):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Id_Type FROM CATEGORIEDECHET WHERE Nom_Type = %s", (nom_dechet,))
    id_type = cursor.fetchone()
    cursor.close()
    return id_type

def insert_dechet(nom, id_type, quantite):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO DECHET(nom_Dechet, id_Type, qte) VALUES (%s, %s, %s)", (nom, id_type, quantite))
    mysql.connection.commit()
    cursor.close()

def get_nom_utilisateur(nom_utilisateur):
    print(f"Recherche de l'utilisateur: {nom_utilisateur}")  # Debug
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nom_Utilisateur FROM UTILISATEUR WHERE nom_Utilisateur = %s", (nom_utilisateur,))
    existing_user = cursor.fetchone()
    cursor.close()
    return existing_user



def get_entreprise(): #choix de l'entreprise
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ENTREPRISE")
    entreprises = cursor.fetchall()
    cursor.close()
    print(entreprises)
    return entreprises
    
def insert_user(nom_utilisateur,mail,numtel,motdepasse,id_entreprise,nom_role):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO UTILISATEUR(nom_Utilisateur,mail,numtel,motdepasse,id_Entreprise,nom_role) VALUES ( %s, %s, %s, %s, %s, %s)", (nom_utilisateur,mail,numtel,motdepasse,id_entreprise,nom_role))
    mysql.connection.commit()
    cursor.close()
     
def get_motdepasse(nom_utilisateur):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT motdepasse FROM UTILISATEUR WHERE nom_Utilisateur = %s", (nom_utilisateur,))
    motdepasse = cursor.fetchone()
    cursor.close()
    return motdepasse[0] if motdepasse else None  # Retourne None si pas d'utilisateur trouvé


