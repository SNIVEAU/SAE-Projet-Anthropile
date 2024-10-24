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

def get_id_type_dechet(nom_dechet):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Id_Type FROM CATEGORIEDECHET WHERE Nom_Type = %s", (nom_dechet,))
    id_type = cursor.fetchone()
    cursor.close()
    return id_type

class PointDeCollecte:
    def __init__(self, id_point_de_collecte, adresse, nom_point, latitude, longitude, quantite_max):
        self.id_point_de_collecte = id_point_de_collecte
        self.adresse = adresse
        self.nom_point = nom_point
        self.latitude = latitude
        self.longitude = longitude
        self.quantite_max = quantite_max

    def __repr__(self):
        return self.nom_point

def get_points_de_collecte():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM POINT_DE_COLLECTE")
    points = cursor.fetchall()
    cursor.close()
    print(points)
    les_points = []
    for id_point_de_collecte, adresse, nom_point, latitude, longitude, quantite_max in points:
        les_points.append(PointDeCollecte(id_point_de_collecte, adresse, nom_point, latitude, longitude, quantite_max))
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

# def data_graph_qte_dechets_categorie():
#     categorie = get_categories()
#     dechets = get_dechets()

#     categorie_data = {}

#     for categorie in categorie:
#         categorie_data[categorie.id_type] = {
#             "nom_type": categorie.nom_type,
#             "quantite": 0, 
#             "dechets": []
#         }
#     print()
#     print(categorie_data)
#     print()

#     for dechet in dechets:
#         if dechet.id_type not in categorie_data:
#             categorie_data[dechet.id_type] = {
#                 "nom_type": dechet.nom_type,
#                 "quantite": 0, 
#                 "dechets": []
#             }
#         categorie_data[dechet.id_type]["quantite"] += dechet.quantite
#         categorie_data[dechet.id_type]["dechets"].append({
#             "nom_dechet": dechet.nom_dechet,
#             "quantite": dechet.quantite
#         })

#     print(categorie_data)

#     data = {
#         'categories': [cat['nom_type'] for cat in categorie_data.values()],
#         'quantities': [cat['quantite'] for cat in categorie_data.values()],
#         'details': [
#             [{'nom': item['nom_dechet'], 'quantite': item['quantite']} for item in cat['dechets']]
#             for cat in categorie_data.values()
#         ]
#     }

#     print()
#     print(data)
#     print()

#     # return categorie_data
#     return jsonify(data)

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

class Traiter:
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
    cursor.execute("SELECT * FROM TRAITER WHERE DATE(dateCollecte) = %s", (date_collecte,))
    traiter = cursor.fetchall()
    cursor.close()
    listetraiter = []
    for i in traiter:
        listetraiter.append(Traiter(i[0], i[1], i[2], i[3]))
    return listetraiter

def get_traiter_sort_by_date():
    cursor = mysql.connection.cursor()
    
    # Sélectionne les colonnes explicitement et formate 'dateCollecte'
    query = """
    SELECT id_point_collecte, id_Type,  DATE_FORMAT(dateCollecte, '%Y-%m-%d') AS date_only,qtecollecte
    FROM TRAITER
    GROUP BY DATE(dateCollecte), id_point_collecte, id_Type
    ORDER BY dateCollecte DESC
    """
    
    cursor.execute(query)
    traiter = cursor.fetchall()
    
    listetraiter = []
    for i in traiter:
        print(i)
        # Remplace les indices selon la position des colonnes sélectionnées
        listetraiter.append(Traiter(i[0], i[1], i[2], i[3]))
    
    cursor.close()
    return listetraiter

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

