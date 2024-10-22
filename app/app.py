from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'c83a8169-f861-4435-ad00-d13f227bc888'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nagarajah:nagarajah@servinfo-maria/DBnagarajah'

db = SQLAlchemy(app)
