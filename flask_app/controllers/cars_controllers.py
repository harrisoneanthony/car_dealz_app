from flask import render_template,redirect,request,session
from flask import flash
from flask_app import app
from flask_app.models.cars_models import Car
from flask_app.controllers import users_controllers

@app.route('/create', methods=['POST'])
def add_car():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
        'price': request.form['price'],
        'user_id': session['user_id']
    }
    if not Car.valdiate_car(data):
        return redirect('/new')
    Car.add_car(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    if 'users_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Car.delete(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':id
    }
    return render_template('edit.html', car = Car.get_one_car(data))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Car.valdiate_car(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'id': id
    }
    Car.update(request.form)
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def show_car(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':id
    }
    car = Car.get_one_car(data)
    return render_template('view.html', car = car)