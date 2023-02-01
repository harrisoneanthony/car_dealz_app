from flask import render_template,redirect,request,session
from flask import flash
from flask_app import app
from flask_app.models.users_models import User
from flask_app.models.cars_models import Car
from flask_app.models import purchases_models
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {"email" : request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/dashboard')

@app.route('/dashboard')
def user():
    if 'user_id' not in session:
        return redirect('/')
    user_in_db = User.get_one({'id':session['user_id']})
    return render_template('dashboard.html', user_in_db=user_in_db, all_cars =  Car.get_all_cars())

@app.route('/logout')
def logout():
    session['user_id'] = ''
    session['first_name'] = ''
    return redirect('/')

@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new.html')

@app.route('/purchase', methods=['POST'])
def purchase():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        "car_id": request.form['car_id']
    }
    purchases_models.Purchase.purchase(data)
    return redirect('/dashboard')

@app.route('/view/purchases')
def view_purchases():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_purchases= User.show_all_purchases(data)
    return render_template('purchases.html', user_in_db = User.get_one(data), all_purchases = all_purchases)