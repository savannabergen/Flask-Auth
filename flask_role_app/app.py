from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    role = request.form['role']

    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()

    flash("Registered successfully. Please Login.")
    return redirect(url_for('login'))

  return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    user = User.query.filter_by(username=request.form['username']).first()
    if user and check_password_hash(user.password, request.form['password']):
      login_user(user)
      return redirect(url_for('dashboard'))
    else:
      flash("Invalid Credentials")

  return render_template('login.html')

if __name__ == '__main__':
  with app.app_context():
    db.create_all
  app.run(debug=True)