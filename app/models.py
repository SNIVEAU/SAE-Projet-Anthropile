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
