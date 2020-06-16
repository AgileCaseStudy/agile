#Importing packages
from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from datetime import datetime
import os


app = Flask(__name__)  #instance init

#DatabaseConfig
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'database.db')


db=SQLAlchemy(app)


#loginpage
@app.route('/', methods=['GET','POST'])
def Login_Page():

    if request.method=='POST':
        UserDetails=request.form
        username=UserDetails['username']
        password=UserDetails['password']
        testuser=Auths.query.filter_by(username=username, password=password).first()
        if testuser:
            designation = int(testuser.usertype)
            loginat=datetime.now().strftime("%B %d, %Y %I:%M%p")
            login_user = Log(username=username,
                             password=password,
                             loginat=loginat)
            db.session.add(login_user)
            db.session.commit()
          
    return render_template('login.html',designation=designation)

#createCustomer
@app.route('/create-customer',methods=['GET','POST'])
def createCustomer():
    if request.method == 'POST':
        return render_template('create-customer.html')

#deleteCustomer
@app.route('/delete-customer',methods=['GET','POST'])
def deleteCustomer():
    return render_template('delete-customer.html')

#database models
class Auths(db.Model):
    __tablename__='auths'
    username=Column(String, primary_key=True, unique=True)
    password=Column(String)
    usertype=Column(Integer)


class Log(db.Model):
    __tablename__='log'
    username=Column(String, primary_key=True, unique=True)
    password=Column(String)
    loginat=Column(String)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
        return render_template('logout.html');
    else:
        return '<p>user already logged out</p>'

app.run(debug=True)
