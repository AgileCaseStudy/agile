#Importing packages
from flask import Flask,render_template,request           
import sqlite3
import os.path

if os.path.isfile('database.db')==False:
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE Auths (username TEXT Primary Key, password TEXT,User_Type INT)')
    conn.close()

app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def Login_Page():
    return render_template('index.html')
    
@app.route('/create-customer',methods=['GET','POST'])
def createCustomer():
        return render_template('create-customer.html')
