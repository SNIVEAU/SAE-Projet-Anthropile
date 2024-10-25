from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = '3ade9a2f-84da-4b64-8b31-8fc35860d740'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


#Mysql configuration

app.config['MYSQL_HOST'] = 'servinfo-maria'
app.config['MYSQL_USER'] = 'lima'
app.config['MYSQL_PASSWORD'] = 'lima'
app.config['MYSQL_DB'] = 'DBlima' #mettre sa propre BD

mysql=MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)