from flask_login import UserMixin
from .app import mysql
import matplotlib.pyplot as plt
import pandas as pd
import os
from flask import jsonify
from .app import app

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
    return les_categories

def get_id_max_dechets():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT MAX(id_Type) FROM CATEGORIEDECHET")
    id_max,  = cursor.fetchone()
    cursor.close()
    return id_max

def insert_categorie(id_type, nom_type):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM CATEGORIEDECHET WHERE id_Type=%s OR nom_Type=%s", (id_type, nom_type))
    company = cursor.fetchone()

    if company:
        cursor.close()
        return False
    else:
        cursor.execute("INSERT INTO CATEGORIEDECHET (id_Type, nom_Type) VALUES (%s, %s)", (id_type, nom_type))
        mysql.connection.commit()
        cursor.close()
        return True

def delete_category(id_type):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM CATEGORIEDECHET NATURAL JOIN DECHET WHERE id_Type=%s", (id_type,))
    dechet_asscocie_categorie = cursor.fetchone()

    cursor.execute("SELECT * FROM COLLECTER WHERE id_Type=%s", (id_type,))

    categorie_dans_collecter = cursor.fetchone()


    if dechet_asscocie_categorie or categorie_dans_collecter:
        cursor.close()
        return False
    else:
        cursor.execute("DELETE FROM CATEGORIEDECHET WHERE id_Type=%s", (id_type,))
        mysql.connection.commit()
        cursor.close()

        return True
    

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

def get_tous_dechets_selon_utilisateur(id):
    cursor = mysql.connection.cursor()
    cursor.execute("select id_Dechet, nom_Dechet, nom_Type, qte from DEPOSER natural join DECHET natural join CATEGORIEDECHET where id_Utilisateur=%s", (id,))
    liste_dechets = cursor.fetchall()
    les_dechets = []
    for id_Dechet, nom_Dechet, nom_Type, qte in liste_dechets:
        les_dechets.append({'nom_dechet': nom_Dechet, 'nom_type': nom_Type, 'quantite': qte})
    return les_dechets

def get_tous_dechets_collectes_selon_utilisateur(id):
    cursor = mysql.connection.cursor()
    cursor.execute("select  nom_dechet, nom_type, quantite from HISTORIQUE_DECHET where id_Utilisateur=%s", (id,))
    liste_dechets = cursor.fetchall()
    les_dechets = []
    for nom_dechet, nom_type, quantite in liste_dechets:
        les_dechets.append({'nom_dechet': nom_dechet, 'nom_type': nom_type, 'quantite': quantite})
    return les_dechets

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
    les_points = []
    for id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude, quantite_max in points:
        les_points.append(PointDeCollecte(id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude, quantite_max))
    return les_points

def get_point_collecte(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM POINT_DE_COLLECTE WHERE id_point_collecte = %s", (id,))
    point = cursor.fetchone()
    cursor.close()
    return PointDeCollecte(point[0], point[1], point[2], point[3], point[4], point[5])

def update_point_collecte(id, adresse, nom_pt_collecte, quantite_max):
    try:
        pos = get_pos_irl(adresse)
        if pos is None:
            return None
        else:
            latitude, longitude = pos
            update_pos_pts_de_collecte(id, latitude, longitude)
    except Exception as e:
        print(f"Erreur lors de la recherche de l'adresse : {adresse}", e)
        return e
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE POINT_DE_COLLECTE SET adresse = %s, nom_pt_collecte = %s, qte_max = %s WHERE id_point_collecte = %s", (adresse, nom_pt_collecte, quantite_max, id))
    mysql.connection.commit()
    cursor.close()
    return True

def delete_point_collecte(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM POINT_DE_COLLECTE WHERE id_point_collecte = %s", (id,))
    mysql.connection.commit()
    cursor.close()

# def 
# -- to install ???
# -- matplotlib pandas

def get_dechets():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM DECHET")
    dechets = cursor.fetchall()
    cursor.close()
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
    return qte_dechets_categorie

def get_graph_qte_dechets_categorie():
    qte_dechets_categorie = get_qte_dechets_categorie()
    nom_types = []
    quantites = []
    for quantite, _, nom_type in qte_dechets_categorie:
        nom_types.append(nom_type)
        quantites.append(quantite)
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
    
    def insert_collecter(self):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO COLLECTER(id_point_collecte, id_Type, dateCollecte, qteCollecte) VALUES (%s, %s, %s, %s)", (self.id_point_collecte, self.id_Type, self.dateCollecte, self.qtecollecte))
        mysql.connection.commit()
        cursor.close()
    
    def __str__(self):
        return str(self.id_point_collecte) + "  " + str(self.id_Type) + self.dateCollecte
def get_collecter():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM COLLECTER")
    collecter = cursor.fetchall()
    cursor.close()
    return collecter

def get_collecter_by_date(date_collecte):
    cursor = mysql.connection.cursor()
    query = """
    SELECT id_point_collecte, id_Type, date_collecte, qtecollecte
    FROM COLLECTER natural join TOURNEE
    WHERE DATE(date_collecte) = %s
    """
    cursor.execute(query, (date_collecte,))
    collecter = cursor.fetchall()
    cursor.close()
    listecollecter = []
    print(collecter)
    for i in collecter:
        print(i)
        print(i[0], i[1], i[2], i[3])
        listecollecter.append(Collecter(i[0], i[1], i[2], i[3]))
    return listecollecter

def get_collecter_sort_by_date():
    cursor = mysql.connection.cursor()
    
    query = """

    SELECT id_point_collecte, id_Type,  DATE_FORMAT(date_collecte, '%Y-%m-%d') AS date_only,qtecollecte
    FROM COLLECTER natural join TOURNEE
    GROUP BY DATE(date_collecte), id_point_collecte, id_Type
    ORDER BY date_collecte DESC
    """
    
    cursor.execute(query)
    collecter = cursor.fetchall()
    
    listecollecter = []
    for i in collecter:

        listecollecter.append(Collecter(i[0], i[1], i[2], i[3]))
    
    cursor.close()
    return listecollecter

def remove_doublon_date_collecter(listecollecte):
    res = []
    hashdate = set()
    for collecte in listecollecte :
        if collecte.dateCollecte not in  hashdate:
            res.append(collecte)
            hashdate.add(collecte.dateCollecte)

    return res

def get_pts_de_collecte_by_adresse(adresse):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM POINT_DE_COLLECTE WHERE adresse = %s", (adresse,))
    points = cursor.fetchall()
    listepoints = []
    for point in points:
        listepoints.append(PointDeCollecte(point[0], point[1], point[2], point[3], point[4], point[5]))

        
    cursor.close()
    return listepoints

def ajoute_pts_de_collecte_specifique(id_pts_de_collecte, id_utilisateur):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO APPARTENIR (id_point_collecte, id_Utilisateur) VALUES (%s, %s)", (id_pts_de_collecte, id_utilisateur))
    mysql.connection.commit()
    cursor.close()

def get_max_id_pts_de_collecte():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT MAX(id_point_collecte) FROM POINT_DE_COLLECTE")
    id_max = cursor.fetchone()
    cursor.close()
    return id_max[0]

def get_max_id_user():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT MAX(id_Utilisateur) FROM UTILISATEUR")
    id_max = cursor.fetchone()
    cursor.close()
    return id_max[0]

def insert_pts_de_collecte(adresse, nom_pt_collecte, 
                           qte_max=500, #Quantité modifiable par défaut
                           pos_x=0, pos_y=0 #Position modifiable par défaut
                           ):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO POINT_DE_COLLECTE(adresse, nom_pt_collecte, pos_x, pos_y, qte_max) VALUES (%s, %s, %s, %s, %s)", (adresse, nom_pt_collecte, pos_x, pos_y, qte_max))
    mysql.connection.commit()
    cursor.close()

    # for pts in get_points_de_collecte():
    #     print(pts.adresse)
    #     try:
    #         latitude, longitude = get_pos_irl(pts.adresse)
    #         print(latitude, longitude)
    #         update_pos_pts_de_collecte(pts.id_point_de_collecte, latitude, longitude)
    #     except Exception as e:
    #         print(f"Erreur lors de la recherche de l'adresse : {pts.adresse}", e)

def get_pos_irl(adresse): 
    from geopy.geocoders import Nominatim
    from .models import get_points_de_collecte

    # les_points_de_collecte = get_points_de_collecte()
    geolocator = Nominatim(user_agent="BIOTRACK'IN/1.0")

    try:
        location = geolocator.geocode(adresse)
        if location:
            print(f"Adresse : {adresse}")
            print(f"Latitude : {location.latitude}, Longitude : {location.longitude}")
            return location.latitude, location.longitude
        else:
            print(f"Adresse non trouvée : {adresse}")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'adresse : {adresse}", e)
        return e
    
def adresse_existante_bd(adresse):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM POINT_DE_COLLECTE WHERE adresse = %s", (adresse,))
    point = cursor.fetchone()
    cursor.close()
    return PointDeCollecte(point[0], point[1], point[2], point[3], point[4], point[5]) if point else None
    # return point

def nom_pt_collecte_existante_bd(nom_pt_collecte):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM POINT_DE_COLLECTE WHERE nom_pt_collecte = %s", (nom_pt_collecte,))
    point = cursor.fetchone()
    cursor.close()
    return PointDeCollecte(point[0], point[1], point[2], point[3], point[4], point[5]) if point else None
    # return point

def update_pos_pts_de_collecte(id, pos_x, pos_y):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE POINT_DE_COLLECTE SET pos_x = %s, pos_y = %s WHERE id_point_collecte = %s", (pos_x, pos_y, id))
    mysql.connection.commit()
    cursor.close()



def get_nom_utilisateur(nom_utilisateur):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nom_Utilisateur FROM UTILISATEUR WHERE nom_Utilisateur = %s", (nom_utilisateur,))
    existing_user = cursor.fetchone()
    cursor.close()
    return existing_user

def get_nom_pts_collecte(nom_pt_collecte):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nom_pt_collecte FROM POINT_DE_COLLECTE WHERE nom_pt_collecte = %s", (nom_pt_collecte,))
    existing_point = cursor.fetchone()
    cursor.close()
    return existing_point

def get_id_utilisateur(nom_utilisateur):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_Utilisateur FROM UTILISATEUR WHERE nom_Utilisateur = %s", (nom_utilisateur,))
    existing_user = cursor.fetchone()
    cursor.close()
    return existing_user[0]
def get_points_de_collecte_by_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
                   '''SELECT 
    P.id_point_collecte, 
    P.adresse, 
    P.nom_pt_collecte, 
    P.pos_x, 
    P.pos_y, 
    P.qte_max,
    A.id_utilisateur
FROM 
    APPARTENIR A
JOIN 
    POINT_DE_COLLECTE P 
ON 
    A.id_point_de_collecte = P.id_point_collecte
WHERE 
    A.id_utilisateur = %s;'''
, (id,))
    points = cursor.fetchall()
    print(points)
    cursor.close()
    les_points = []
    for id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude,quantite_max,_ in points:
        les_points.append(PointDeCollecte(id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude, quantite_max))
    print(les_points)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM POINT_DE_COLLECTE")
    points = cursor.fetchall()
    for id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude, quantite_max in points:
        if not id_point_de_collecte in [point.id_point_de_collecte for point in les_points]:
            les_points.append(PointDeCollecte(id_point_de_collecte, adresse, nom_pt_collecte, latitude, longitude, quantite_max))
    
    cursor.close()
    print(les_points)
    return les_points

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
    return entreprises

def get_entreprise_sous_forme_classe():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ENTREPRISE order by id_entreprise")
    entreprises = cursor.fetchall()
    cursor.close()
    ents =[]
    for id_entreprise, nom_entreprise in entreprises:
        ents.append(Entreprise(id_entreprise, nom_entreprise))
    return ents

def get_entreprise_par_id(id):
    entreprises=get_entreprise_sous_forme_classe()
    for entreprise in entreprises:
        if entreprise.id_entreprise == id:
            return entreprise

def get_id_max_entreprise():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT max(id_entreprise) FROM ENTREPRISE")
    id_max = cursor.fetchone()[0]
    cursor.close()
    return id_max
        
def update_entreprise(id, nom):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ENTREPRISE WHERE nom_entreprise=%s", (nom,))
    ent = cursor.fetchone()
    if ent:
        cursor.close()
        return False
    else:
        cursor.execute("UPDATE ENTREPRISE SET nom_entreprise=%s WHERE id_entreprise=%s", (nom, id))
        mysql.connection.commit()
        cursor.close()
        return True

def delete_company(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ENTREPRISE NATURAL JOIN TRAVAILLER NATURAL JOIN UTILISATEUR WHERE id_entreprise=%s", (id,))
    utilisateur_avec_entreprise = cursor.fetchone()

    if utilisateur_avec_entreprise:
        cursor.close()
        return False
    else:
        cursor.execute("DELETE FROM ENTREPRISE WHERE id_entreprise=%s", (id,))
        mysql.connection.commit()
        cursor.close()
        return True
    
def insert_entreprise(id, nom):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ENTREPRISE WHERE id_entreprise=%s OR nom_entreprise=%s", (id, nom))
    ent = cursor.fetchone()

    if ent:
        cursor.close()
        return False
    else:
        cursor.execute("INSERT INTO ENTREPRISE (id_entreprise, nom_entreprise) VALUES (%s, %s)", (id, nom))
        mysql.connection.commit()
        cursor.close()
        return True
    
    
def get_all_user_info(user_name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM UTILISATEUR WHERE nom_Utilisateur = %s", (user_name,))
    user_data = cursor.fetchone()
    cursor.close()
    return user_data

def update_user(user_id, nom_utilisateur, mail, numtel):
    cursor = mysql.connection.cursor()
    
    query = """
        UPDATE UTILISATEUR
        SET nom_utilisateur = %s, mail = %s, numtel = %s
        WHERE id_utilisateur = %s
    """
    
    cursor.execute(query, (nom_utilisateur, mail, numtel, user_id))
    
    mysql.connection.commit()
    
    cursor.close()



def update_password(user_id,password):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE UTILISATEUR SET motdepasse = %s WHERE id_Utilisateur = %s", (password,user_id))
    mysql.connection.commit()
    cursor.close()
    

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

class Avis:
    def __init__(self, id_avis, nom_utilisateur, avis, note, date_avis):
        self.id_avis = id_avis
        self.nom_utilisateur = nom_utilisateur
        self.avis = avis
        self.note = note
        self.date_avis = date_avis

    def __repr__(self):
        return self.nom_utilisateur + " : " + self.avis

def get_avis():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_Avis, nom_Utilisateur, avis, note, DATE_FORMAT(date_Avis, '%d/%m/%Y') FROM AVIS NATURAL JOIN UTILISATEUR ORDER BY date_Avis DESC")
    avis = cursor.fetchall()
    cursor.close()
    les_avis = []
    for id_avis, nom_utilisateur, avis, note, date_avis in avis:
        les_avis.append(Avis(id_avis, nom_utilisateur, avis, note, date_avis))
    return les_avis

def get_global_note():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT AVG(note) FROM AVIS")
    note = cursor.fetchone()
    cursor.close()
    if note[0] is None:
        return 5
    return note[0]

def insert_avis(id_utilisateur, avis, note):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO AVIS(id_Utilisateur, avis, note) VALUES (%s, %s, %s)", (id_utilisateur, avis, note))
    mysql.connection.commit()
    cursor.close()

def get_id_avis(nom_utilisateur, avis, date_avis):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id_Avis FROM AVIS
        WHERE nom_Utilisateur = %s AND avis = %s AND date_Avis = STR_TO_DATE(%s, '%d/%m/%Y')
    """, (nom_utilisateur, avis, date_avis))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0]  # Retourne l'ID de l'avis
    return None  # Si aucun avis trouvé, retourne None

def delete_avis_id(ids):
    if not ids:
        return 0
    try:
        cursor = mysql.connection.cursor()
        # format_strings = ', '.join(['%s'] * len(ids))  # Crée une chaîne de format pour la requête
        query = f"DELETE FROM AVIS WHERE id_Avis IN ({ids})"
        cursor.execute(query)
        mysql.connection.commit()
        deleted_count = cursor.rowcount
        cursor.close()
        return deleted_count
    except Exception as e:
        print(f"Erreur lors de la suppression des avis : {e}")
        return 0


def insert_collecter(id_point_collecte, id_tournee, id_type, qte_collecte):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO COLLECTER (id_point_collecte, id_Tournee, id_Type, qtecollecte)
        VALUES (%s, %s, %s, %s)
        """, 
        (id_point_collecte, id_tournee, id_type, qte_collecte)
    )
    mysql.connection.commit()
    cursor.close()


    
def get_qte_collecte_by_categories(id_type):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT SUM(qteCollecte) FROM COLLECTER WHERE id_Type = %s", (id_type,))
    qte_collecte = cursor.fetchone()
    cursor.close()
    return qte_collecte[0]

def insert_tournee(date_collecte, duree=0):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO TOURNEE(date_collecte, duree) VALUES (%s, %s)", (date_collecte, duree))
    mysql.connection.commit()
    cursor.close()


def get_last_tournee():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT MAX(id_tournee) FROM TOURNEE")
    id_tournee = cursor.fetchone()
    cursor.close()
    return id_tournee[0]

def get_qte_by_pts_and_type(id_point_collecte, id_type):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT quantite_point_collecte_filtree(%s, %s)", (id_point_collecte, id_type))
    qte_collecte = cursor.fetchone()
    cursor.close()
    return qte_collecte[0] if qte_collecte else 0

