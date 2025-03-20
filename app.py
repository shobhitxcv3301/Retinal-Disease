from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.secret_key = 'secretkey'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, name, email, mobile_number,gender,age,password):
        self.name = name
        self.email = email
        self.mobile_number = mobile_number
        self.gender = gender
        self.age = age
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
with app.app_context():
    db.create_all()
    


@app.route('/')
def home():
    return render_template('Landingpage.html')

@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                print("loged in")
                session['email'] = user.email
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html',message='Invalid password')
        else:
            return render_template('login.html',message='User not found')   
    return render_template('login.html')

@app.route('/Landingpage')
def Landingpage():
    return render_template('Landingpage.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        gender = request.form['gender']
        age = request.form['age']
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return render_template('register.html',message='User already exists')
        except:
            pass
        user = User(name=name,email=email,mobile_number=mobile_number,password=password,gender=gender,age=age)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    if session["email"]:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    return redirect(url_for('login'))

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')


if __name__=='__main__':
    app.run(debug=True)