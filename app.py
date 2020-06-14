from flask import Flask,render_template            #Importing packages

app = Flask(__name__)
@app.route('/')
def Login_Page():
    return render_template('Login.html')
