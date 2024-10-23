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

def get_traiter_sort_by_date():
    cursor = mysql.connection.cursor()
    
    query = """
    SELECT * FROM TRAITER
    GROUP BY DATE(dateCollecte)
    ORDER BY dateCollecte DESC
    """
    
    cursor.execute(query)
    traiter = cursor.fetchall()
    
    listetraiter = []
    for i in traiter:
        listetraiter.append(Traiter(i[0], i[1], i[2], i[3]))
    
    cursor.close()
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
