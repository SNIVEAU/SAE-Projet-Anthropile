from .app import mysql

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

    def __init__(self, id_dechet, nom_dechet, id_type, quantite):
        self.id_dechet = id_dechet
        self.nom_dechet = nom_dechet
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