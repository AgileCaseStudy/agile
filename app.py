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
          
    return render_template('login.html')

#check_user
@app.route('/check_user', methods=['GET','POST'])
def check_user():
    if request.method=='POST':
        UserDetails=request.form
        username=UserDetails['username']
        password=UserDetails['password']
        testuser=Auths.query.filter_by(username=username, password=password).first()
        if testuser:
            designation = int(testuser.usertype)
            if designation==0:
                return render_template('create-customer.html')
            else:
                return 'You are a cashier/Teller.'

#createCustomer
@app.route('/create-customer',methods=['GET','POST'])
def createCustomer():
    errormsg=''
    if request.method=='POST':
        CustDetails=request.form
        ws_ssn=CustDetails['ws_ssn']
        ws_name=CustDetails['ws_name']
        ws_age=CustDetails['ws_age']
        ws_adrs=CustDetails['ws_adrs_1']+" "+CustDetails['ws_adrs_2']+" "+CustDetails['ws_state']+" "+CustDetails['ws_city']
        testssn=Auths.query.filter_by(ws_ssn=ws_ssn).first()
        if testssn:
            errormsg='exists'
        else:
            create_cus = CustDetails(ws_ssn=ws_ssn,
                                     ws_name=ws_name,
                                     ws_age=ws_age,
                                     ws_adrs=ws_adrs)
            db.session.add(create_cus)
            db.session.commit()
            errormsg='success'
    return render_template('create-customer.html',errormsg=errormsg)


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

class CustDetails(db.Model):
    __tablename__='custdetails'
    ws_ssn=Column(Integer, primary_key=True, unique=True)
    ws_name=Column(String)
    ws_age=int(Column(Integer))
    ws_adrs=Column(String)


@app.route('/logout')
def logout():
        return render_template('logout.html');
    

    
app.run(debug=True)
