from flask_login import UserMixin
from .app import mysql
import matplotlib.pyplot as plt
import pandas as pd
import os
from flask import jsonify

# def get_id_max_dechets():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT MAX(id_Dechet) FROM DECHET")
#     id_max,  = cursor.fetchone()
#     cursor.close()
#     print(id_max, "*********")
#     return id_max

class CategorieDechet:
    def __init__(self, id_type, nom_type):
        self.id_type = id_type
        self.nom_type = nom_type

    def __repr__(self):
        return self.nom_type

def get_categories():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM CATEGORIEDECHET")
    categories = cursor.fetchall()
    cursor.close()
    les_categories = []
    for id_categorie, nom_categorie in categories:
        les_categories.append(CategorieDechet(id_categorie, nom_categorie))
    for categorie in les_categories:
        print(type(categorie))
    print(categories, les_categories)
    # return categories
    return les_categories

class Dechet:
    def __init__(self, nom_dechet, id_type, quantite):
        self.nom_dechet = nom_dechet
        if type(id_type) == str:
            self.id_type = get_id_type_dechet(id_type)
        else:
            self.id_type = id_type
        self.quantite = quantite

    def __repr__(self):
        return self.nom_dechet
    
    def insert_dechet(self):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO DECHET(nom_Dechet, id_Type, qte) VALUES (%s, %s, %s)", (self.nom_dechet, self.id_type, self.quantite))
        mysql.connection.commit()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT MAX(id_Dechet) FROM DECHET")
        id_max,  = cursor.fetchone()
        cursor.close()
        return id_max

def insert_dechet_utilisateur(id_dechet, id_utilisateur, id_point_collecte):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO DEPOSER(id_Dechet, id_Utilisateur, id_point_collecte) VALUES (%s, %s, %s)", (id_dechet, id_utilisateur, id_point_collecte))
    mysql.connection.commit()
    cursor.close()

def get_id_type_dechet(nom_dechet):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Id_Type FROM CATEGORIEDECHET WHERE Nom_Type = %s", (nom_dechet,))
    id_type = cursor.fetchone()
    cursor.close()
    return id_type

class PointDeCollecte:
    def __init__(self, id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude, quantite_max):
        self.id_point_de_collecte = id_point_de_collecte
        self.adresse = adresse
        self.nom_pt_collecte = nom_pt_collecte
        self.latitude = latitude
        self.longitude = longitude
        self.quantite_max = quantite_max

    def __repr__(self):
        return self.nom_pt_collecte

def get_points_de_collecte():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM POINT_DE_COLLECTE")
    points = cursor.fetchall()
    cursor.close()
    print(points)
    les_points = []
    for id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude, quantite_max in points:
        les_points.append(PointDeCollecte(id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude, quantite_max))
    print(les_points)
    # return points
    return les_points

# def 
# -- to install ???
# -- matplotlib pandas

def get_dechets():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM DECHET")
    dechets = cursor.fetchall()
    cursor.close()
    print(dechets)
    les_dechets = []
    for _, nom_dechet, id_type, quantite in dechets:
        les_dechets.append(Dechet(nom_dechet, id_type, quantite))
    return les_dechets

def get_graph_dechet():
    dechets = get_dechets()
    nom_dechets = []
    quantites = []
    for dechet in dechets:
        nom_dechets.append(dechet.nom_dechet)
        quantites.append(dechet.quantite)
    print(nom_dechets, quantites)
    plt.bar(nom_dechets, quantites)
    plt.xlabel("Déchets")
    plt.ylabel("Quantité")
    plt.title("Quantité de déchets")

    chemin_img = os.path.join('static', 'img', 'graph_dechets.png')
    plt.savefig(chemin_img)
    plt.close()

def get_qte_dechets_categorie():
    cursor = mysql.connection.cursor()
    cursor.execute("select SUM(qte) as quantite, id_Type, nom_Type from DECHET NATURAL join CATEGORIEDECHET GROUP BY id_Type")
    qte_dechets_categorie = cursor.fetchall()
    cursor.close()
    print(qte_dechets_categorie)
    return qte_dechets_categorie

def get_graph_qte_dechets_categorie():
    qte_dechets_categorie = get_qte_dechets_categorie()
    nom_types = []
    quantites = []
    for quantite, _, nom_type in qte_dechets_categorie:
        nom_types.append(nom_type)
        quantites.append(quantite)
    print(nom_types, quantites)
    plt.bar(nom_types, quantites)
    plt.xlabel("Catégories de déchets")
    plt.ylabel("Quantité")
    plt.title("Quantité de déchets par catégorie")

    chemin_img = os.path.join('static', 'img', 'graph_qte_dechets_categorie.png')
    plt.savefig(chemin_img)
    plt.close()

def data_graph_qte_dechets_categorie():
    categories = get_categories()
    dechets = get_dechets()

    # Initialize data structure for categories
    category_data = {cat.id_type: {'nom_type': cat.nom_type, 'quantite': 0, 'dechets': []} for cat in categories}

    # Populate quantities and details
    for dechet in dechets:
        category_data[dechet.id_type]['quantite'] += dechet.quantite
        category_data[dechet.id_type]['dechets'].append({'nom_dechet': dechet.nom_dechet, 'quantite': dechet.quantite})

    data = {
        'categories': [cat['nom_type'] for cat in category_data.values()],
        'quantities': [cat['quantite'] for cat in category_data.values()],
        'details': [[{'nom': item['nom_dechet'], 'quantite': item['quantite']} for item in cat['dechets']]
                    for cat in category_data.values()]
    }

    return jsonify(data)

class Collecter:
    def __init__(self, id_point_collecte,id_Type,dateCollecte,qtecollecte):
        self.id_point_collecte = id_point_collecte
        self.id_Type = id_Type
        self.dateCollecte = dateCollecte
        self.qtecollecte = qtecollecte
    
    def insert_traiter(self):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO TRAITER(id_Point_Collecte, id_Type, dateCollecte, qteCollecte) VALUES (%s, %s, %s, %s)", (self.id_point_collecte, self.id_Type, self.dateCollecte, self.qtecollecte))
        mysql.connection.commit()
        cursor.close()

def get_traiter():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM TRAITER")
    traiter = cursor.fetchall()
    cursor.close()
    return traiter

def get_traiter_by_date(date_collecte):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_point_collecte,id_Type,date_collecte,qtecollecte FROM COLLECTER natural join TOURNEE WHERE DATE(date_collecte) = %s", (date_collecte,))
    traiter = cursor.fetchall()
    cursor.close()
    listetraiter = []
    for i in traiter:
        listetraiter.append(Collecter(i[0], i[1], i[2], i[3]))
    return listetraiter


def get_pts_de_collecte_by_adresse(adresse):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM POINT_DE_COLLECTE WHERE adresse = %s", (adresse,))
    points = cursor.fetchall()
    listepoints = []
    for point in points:
        listepoints.append(PointDeCollecte(point[0], point[1], point[2], point[3], point[4], point[5]))

        
    cursor.close()
    return listepoints


def insert_pts_de_collecte(adresse, nom_pt_collecte, pos_x, pos_y, 
                           qte_max=500 #Quantité modifiable par défaut
                           ):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO POINT_DE_COLLECTE(adresse, nom_pt_collecte, pos_x, pos_y, qte_max) VALUES (%s, %s, %s, %s, %s)", (adresse, nom_pt_collecte, pos_x, pos_y, qte_max))
    mysql.connection.commit()
    cursor.close()

def get_traiter_sort_by_date():
    cursor = mysql.connection.cursor()
    
    # Sélectionne les colonnes explicitement et formate 'dateCollecte'
    query = """
    SELECT id_point_collecte, id_Type,  DATE_FORMAT(date_collecte, '%Y-%m-%d') AS date_only,qtecollecte
    FROM COLLECTER natural join TOURNEE
    GROUP BY DATE(date_collecte), id_point_collecte, id_Type
    ORDER BY date_collecte DESC
    """
    
    cursor.execute(query)
    traiter = cursor.fetchall()
    
    listetraiter = []
    for i in traiter:
        print(i)
        # Remplace les indices selon la position des colonnes sélectionnées
        listetraiter.append(Collecter(i[0], i[1], i[2], i[3]))
    
    cursor.close()
    return listetraiter

def get_nom_utilisateur(nom_utilisateur):
    print(f"Recherche de l'utilisateur: {nom_utilisateur}")  # Debug
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nom_Utilisateur FROM UTILISATEUR WHERE nom_Utilisateur = %s", (nom_utilisateur,))
    existing_user = cursor.fetchone()
    cursor.close()
    return existing_user

def get_id_utilisateur(nom_utilisateur):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_Utilisateur FROM UTILISATEUR WHERE nom_Utilisateur = %s", (nom_utilisateur,))
    existing_user = cursor.fetchone()
    cursor.close()
    return existing_user[0]

class Entreprise:
    def __init__(self, id_entreprise, nom_entreprise):
        self.id_entreprise = id_entreprise
        self.nom_entreprise = nom_entreprise
    def __str__(self):
        return self.nom_entreprise

def get_entreprise_register():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ENTREPRISE")
    entreprises = cursor.fetchall()
    cursor.close()
    return [(e[0],e[1]) for e in entreprises]+[('Aucune', 'Aucune')] 


def get_entreprise(): #choix de l'entreprise
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ENTREPRISE")
    entreprises = cursor.fetchall()
    cursor.close()
    print(entreprises)
    return entreprises
    

def get_all_user_info(user_name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM UTILISATEUR WHERE nom_Utilisateur = %s", (user_name,))
    user_data = cursor.fetchone()
    cursor.close()
    return user_data 
def insert_user(nom_utilisateur,mail,numtel,motdepasse,nom_role):

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO UTILISATEUR(nom_Utilisateur,mail,numtel,motdepasse,nom_role) VALUES ( %s, %s, %s, %s, %s)", (nom_utilisateur,mail,numtel,motdepasse,nom_role))
    mysql.connection.commit()
    cursor.close()
     
def insert_travailler(id_Utilisateur,id_entreprise):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO TRAVAILLER(id_utilisateur,id_Entreprise) VALUES (%s, %s)", (id_Utilisateur,id_entreprise))
    mysql.connection.commit()
    cursor.close()

def get_motdepasse(nom_utilisateur):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT motdepasse FROM UTILISATEUR WHERE nom_Utilisateur = %s", (nom_utilisateur,))
    motdepasse = cursor.fetchone()
    cursor.close()
    return motdepasse[0] if motdepasse else None  # Retourne None si pas d'utilisateur trouvé

def data_graph_qte_dechets_cat_pts_collecte():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT nom_pt_collecte, nom_Type, SUM(qte) as quantite
        FROM POINT_DE_COLLECTE 
        NATURAL JOIN CATEGORIEDECHET 
        NATURAL JOIN DECHET 
        NATURAL JOIN DEPOSER 
        GROUP BY nom_pt_collecte, nom_Type 
        ORDER BY nom_pt_collecte;
    """)
    results = cursor.fetchall()
    cursor.close()

    data = {}
    for nom_pt_collecte, nom_type, quantite in results:
        if nom_pt_collecte not in data:
            data[nom_pt_collecte] = []
        data[nom_pt_collecte].append({'categorie': nom_type, 'quantite': quantite})

    return jsonify(data)

def get_quantite_courante(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT IFNULL(SUM(qte),0) FROM DEPOSER NATURAL JOIN DECHET NATURAL JOIN POINT_DE_COLLECTE WHERE id_point_collecte = %s", (id,))
    quantite_courante = cursor.fetchone()
    cursor.close()
    return quantite_courante[0]

def get_pts_collecte_and_id():
    pts_de_collecte = get_points_de_collecte()
    choices = []
    for point in pts_de_collecte:
        choices.append((point.id_point_de_collecte, point))
    return choices

#class Collecter:
#    def __init__(self, id_point_collecte,id_Tournee, id_Type, qtecollecte):
#        self.id_point_collecte = id_point_collecte
#        self.id_Tournee = id_Tournee
#        self.id_Type = id_Type
#        self.qtecollecte = qtecollecte
#    
#    def __init__(self, date_collecte, nom_Type, qtecollecte, duree):
#        self.date_collecte = date_collecte
#        self.nom_Type = nom_Type
#        self.qtecollecte = qtecollecte
#        self.duree = duree
#    

def get_liste_collectes(id):
    cursor = mysql.connection.cursor()
    cursor.execute("select date_collecte, nom_Type, qtecollecte, duree from COLLECTER natural join CATEGORIEDECHET natural join TOURNEE where id_point_collecte=%s", (id,))
    liste_collectes = cursor.fetchall()
    cursor.close()
    collectes = []
    for date_collecte, nom_Type, qtecollecte, duree in liste_collectes:
        collectes.append({'date_collecte': date_collecte, 'nom_Type': nom_Type, 'qtecollecte' :qtecollecte, 'duree': duree})
    return collectes

