#Importing packages
from flask import Flask,render_template,request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from datetime import datetime
import os


app = Flask(__name__)  #instance init
app.secret_key = '#12345678'


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
        session['username']=request.form['username']
        testuser=Auths.query.filter_by(username=username, password=password).first()
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
            loginat=datetime.now().strftime("%B %d, %Y %I:%M%p")
            login_user = Log(username=username,
                             password=password,
                             loginat=loginat)
            db.session.add(login_user)
            db.session.commit()
            if designation==0:
                return redirect(url_for('createCustomer'))
            else:
                return 'You are a cashier/Teller.'


#createCustomer
ccustid=100000000
@app.route('/create-Customer',methods=['GET','POST'])
def createCustomer():
    msg=''
    if request.method=='POST':
        #CustDetails=request.form
        ws_ssn=request.form['ws_ssn']
        ws_name=request.form['ws_name']
        ws_age=request.form['ws_age']
        ws_adrs=request.form['ws_adrs_1']
        testssn=CustDetails.query.filter_by(ws_ssn=ws_ssn).first()
        if testssn:
            msg='exists'
            return render_template('create-customer.html',msg=msg),409
        else:
            global ccustid
            ccustid = ccustid+1
            ws_cust_id=ccustid
            create_cus = CustDetails(ws_ssn=ws_ssn,
                                     ws_name=ws_name,
                                     ws_age=ws_age,
                                     ws_adrs=ws_adrs,
                                     ws_cust_id=ws_cust_id)
            db.session.add(create_cus)
            db.session.commit()
            msg='success'
            return render_template('create-customer.html',msg=msg),201
    return render_template('create-customer.html')


#updatesearchCustomer
@app.route('/update-search-customer',methods=['GET','POST'])
def uSearchCustomer():
    if request.method=='POST':
        updateCustomer=request.form
        ws_ssn=updateCustomer['ws_ssn']
        ws_cust_id=updateCustomer['ws_cust_id']
        testexists=CustDetails.query.filter_by(ws_ssn=ws_ssn, ws_cust_id=ws_cust_id).first()
        if testexists:
            ws_ssn = testexists.ws_ssn
            ws_cust_id = testexists.ws_cust_id
            ws_name = testexists.ws_name
            ws_adrs = testexists.ws_adrs
            ws_age = testexists.ws_age
            return render_template('update-customer.html',ws_ssn=ws_ssn,ws_cust_id=ws_cust_id,ws_name=ws_name,ws_adrs=ws_adrs,ws_age=ws_age)
    return render_template('update-search-customer.html'),202


#deletesearchCustomer
@app.route('/delete-search-customer', methods=['GET','POST'])
def dSearchCustomer():
    if request.method=='POST':
        ws_ssn=request.form['ws_ssn']
        ws_cust_id=request.form['ws_cust_id']
        if (type(ws_ssn)==str):
            testexists=CustDetails.query.filter_by(ws_ssn=ws_ssn).first()
            ws_ssn=testexists.ws_ssn
            ws_cust_id=testexists.ws_cust_id
            ws_name=testexists.ws_name
            ws_adrs = testexists.ws_adrs
            ws_age = testexists.ws_age
            return render_template('delete-customer.html',ws_ssn=ws_ssn,ws_cust_id=ws_cust_id,ws_name=ws_name,ws_adrs=ws_adrs,ws_age=ws_age)
        elif (type(ws_cust_id)==str) :
            testexists=CustDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
            ws_ssn=testexists.ws_ssn
            ws_cust_id=testexists.ws_cust_id
            ws_name=testexists.ws_name
            ws_adrs = testexists.ws_adrs
            ws_age = testexists.ws_age
            return render_template('delete-customer.html',ws_ssn=ws_ssn,ws_cust_id=ws_cust_id,ws_name=ws_name,ws_adrs=ws_adrs,ws_age=ws_age)
    return render_template('delete-search-customer.html')


#updateCustomer
@app.route('/update-customer', methods=['GET','POST'])
def updateCustomer():
    if request.method=='POST' and 'new_ws_name' in request.form():
        new_ws_name=request.form['new_ws_name']
        new_ws_adrs=request.form['new_ws_adrs']
        new_ws_age=request.form['new_ws_age']
        update_cus=CustDetails(ws_name=new_ws_name,
                               ws_adrs=new_ws_adrs,
                               ws_age=new_ws_age)
        db.session.add(update_cus)
        db.session.commit()
        msg='success'
        return render_template('update-customer.html',msg=msg),200
    return render_template('update-customer.html')


#deleteCustomer
@app.route('/delete-customer',methods=['GET','POST'])
def deleteCustomer():
    if request.method=='POST':
        ws_ssn=request.form['ws_ssn']
        delcus=CustDetails.query.filter_by(ws_ssn=ws_ssn).first()
        if delcus:
            db.session.delete(delcus)
            db.session.commit()
            msg='success'
            return render_template('delete-customer.html',msg=msg),200
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
    ws_ssn=Column(String, primary_key=True)
    ws_name=Column(String)
    ws_age=Column(String)
    ws_adrs=Column(String)
    ws_cust_id=Column(Integer)



@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
        return render_template('logout.html');
    else:
        return '<p>user already logged out</p>'



app.run(debug=True)
