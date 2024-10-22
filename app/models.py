# from .app import db

# def get_categories():
#     return db.session.query(CategoriesDechets).all()

# class Dechets(db.Model):
#     __tablename__ = "DECHET"

#     id_Dechet = db.Column(db.Integer, primary_key=True)
#     nom_Dechet = db.Column(db.String(100), nullable=False)
#     Id_Type = db.Column(db.Integer, db.ForeignKey("CategoriesDechets.Id_Type"), nullable=False) # id_category donc relation avec la table CategoriesDechets (relationship)
#     volume = db.Column(db.Integer, nullable=False)

#     identifiant_type = db.relationship("CategoriesDechets", backref="dechets")

#     def __init__(self, id_Dechet, nom_Dechet, id_Type, volume):
#         self.id_Dechet = id_Dechet
#         self.nom_Dechet = nom_Dechet
#         self.id_Type = id_Type
#         self.volume = volume

#     def __repr__(self):
#         return f"Dechet('{self.nom_Dechet}', '{self.volume}')"

# class CategoriesDechets(db.Model):
#     __tablename__ = "CATEGORIEDECHET"

#     Id_Type = db.Column(db.Integer, primary_key=True)
#     Nom_Type = db.Column(db.String(100), nullable=False)



#     def __init__(self, Id_Type, Nom_Type):
#         self.Id_Type = Id_Type
#         self.Nom_Type = Nom_Type

#     def __repr__(self):
#         return f"CategoriesDechets('{self.Nom_Type}')"
    
from .app import db

class CategoriesDechets(db.Model):
    __tablename__ = "CATEGORIEDECHET"

    Id_Type = db.Column(db.Integer, primary_key=True)
    Nom_Type = db.Column(db.String(100), nullable=False)

    def __init__(self, Id_Type, Nom_Type):
        self.Id_Type = Id_Type
        self.Nom_Type = Nom_Type

    def __repr__(self):
        return f"CategoriesDechets('{self.Nom_Type}')"

def get_categories():
    return db.session.query(CategoriesDechets).all()

class Dechets(db.Model):
    __tablename__ = "DECHET"

    id_Dechet = db.Column(db.Integer, primary_key=True)
    nom_Dechet = db.Column(db.String(100), nullable=False)
    Id_Type = db.Column(db.Integer, db.ForeignKey("CATEGORIEDECHET.Id_Type"), nullable=False)
    qte = db.Column(db.Integer, nullable=False)

    identifiant_type = db.relationship("CategoriesDechets", backref="dechets")

    def __init__(self, id_Dechet, nom_Dechet, Id_Type, qte): 
        self.id_Dechet = id_Dechet
        self.nom_Dechet = nom_Dechet
        self.Id_Type = Id_Type 
        self.qte = qte

    def __repr__(self):
        return f"Dechet('{self.nom_Dechet}', '{self.qte}')"
