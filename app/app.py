from flask import Flask
# from sqlalchemy import *
# import os
# import MySQLdb
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'c83a8169-f861-4435-ad00-d13f227bc888'

# db = MySQLdb.connect(
#     host="servinfo-maria",
#     user="nagarajah",
#     passwd="nagarajah",
#     db="DBnagarajah"
# )

# print(db, "***********")

# # requete : 
# cursor = db.cursor()
# cursor.execute("SELECT * FROM CATEGORIEDECHET")
# result = cursor.fetchall()
# print(result)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nagarajah:nagarajah@servinfo-maria/DBnagarajah'

db = SQLAlchemy(app)
