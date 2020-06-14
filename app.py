from flask import Flask,render_template,request           
#Importing packages

app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def Login_Page():
    if request.method == 'POST':
        return render_template('index.html')
    
@app.route('/create-customer',methods=['GET','POST'])
def create-customer():
    if request.method == 'POST':
        return render_template('create-customer.html')
