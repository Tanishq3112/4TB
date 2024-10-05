from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import WorkoutForm, MealForm, ActivityForm, LoginForm, RegistrationForm  # Ensure these forms exist

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if unauthorized

# Define your models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # In a real app, this should be hashed

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

# Create database and tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

# ---------- Authentication Routes ----------

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # In a real app, hash the password
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('workouts'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=form.username.data, password=form.password.data)  # Hash password in a real app
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ---------- Workouts Section ----------

@app.route('/workouts', methods=['GET', 'POST'])
@login_required
def workouts():
    form = WorkoutForm()
    if form.validate_on_submit():
        new_workout = Workout(name=form.name.data, duration=form.duration.data)
        db.session.add(new_workout)
        db.session.commit()
        flash('Workout added successfully!', 'success')
        return redirect(url_for('workouts'))

    workouts = Workout.query.all()
    return render_template('workouts.html', form=form, workouts=workouts)

@app.route('/workouts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_workout(id):
    workout = Workout.query.get_or_404(id)
    form = WorkoutForm(obj=workout)
    
    if form.validate_on_submit():
        workout.name = form.name.data
        workout.duration = form.duration.data
        db.session.commit()
        flash('Workout updated successfully!', 'success')
        return redirect(url_for('workouts'))

    return render_template('edit_workout.html', form=form, workout=workout)

@app.route('/workouts/delete/<int:id>', methods=['POST'])
@login_required
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully!', 'success')
    return redirect(url_for('workouts'))

# ---------- Meals Section ----------

@app.route('/meals', methods=['GET', 'POST'])
@login_required
def meals():
    form = MealForm()
    if form.validate_on_submit():
        new_meal = Meal(name=form.name.data, calories=form.calories.data)
        db.session.add(new_meal)
        db.session.commit()
        flash('Meal added successfully!', 'success')
        return redirect(url_for('meals'))

    meals = Meal.query.all()
    return render_template('meals.html', form=form, meals=meals)

@app.route('/meals/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_meal(id):
    meal = Meal.query.get_or_404(id)
    form = MealForm(obj=meal)
    
    if form.validate_on_submit():
        meal.name = form.name.data
        meal.calories = form.calories.data
        db.session.commit()
        flash('Meal updated successfully!', 'success')
        return redirect(url_for('meals'))

    return render_template('edit_meal.html', form=form, meal=meal)

@app.route('/meals/delete/<int:id>', methods=['POST'])
@login_required
def delete_meal(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    flash('Meal deleted successfully!', 'success')
    return redirect(url_for('meals'))

# ---------- Activities Section ----------

@app.route('/activity', methods=['GET', 'POST'])
@login_required
def activity():
    form = ActivityForm()
    if form.validate_on_submit():
        new_activity = Activity(description=form.description.data, duration=form.duration.data)
        db.session.add(new_activity)
        db.session.commit()
        flash('Activity added successfully!', 'success')
        return redirect(url_for('activity'))

    activities = Activity.query.all()
    return render_template('activity.html', form=form, activities=activities)

@app.route('/activity/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_activity(id):
    activity = Activity.query.get_or_404(id)
    form = ActivityForm(obj=activity)
    
    if form.validate_on_submit():
        activity.description = form.description.data
        activity.duration = form.duration.data
        db.session.commit()
        flash('Activity updated successfully!', 'success')
        return redirect(url_for('activity'))

    return render_template('edit_activity.html', form=form, activity=activity)

@app.route('/activity/delete/<int:id>', methods=['POST'])
@login_required
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    flash('Activity deleted successfully!', 'success')
    return redirect(url_for('activity'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Updated to run on all interfaces
