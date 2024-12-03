from flask import Flask, jsonify, render_template, redirect, url_for, request, session
from admin_dashboarddb import get_total_spots, get_total_e_waste, get_total_users, get_collection_spots, get_e_waste_items
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirects to login if not logged in
bcrypt = Bcrypt(app)


# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, role FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return User(id=user_data[0], username=user_data[1], role=user_data[2])
    return None


@app.route('/')
def root():
    # Redirect unauthenticated users to login
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, password, role FROM users WHERE name = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and bcrypt.check_password_hash(user_data[2], password):
            user = User(id=user_data[0], username=user_data[1], role=user_data[3])
            login_user(user)
            return redirect(url_for('index'))
        return "Invalid credentials", 401
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                       (username, email, hashed_password, role))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/admin')
@login_required
def admin_dashboard():
    total_spots = get_total_spots()
    total_e_waste = get_total_e_waste()
    total_users = get_total_users()
    collection_spots = get_collection_spots()
    e_waste_items = get_e_waste_items()
    return render_template('admin.html',
                           total_spots=total_spots,
                           total_e_waste=total_e_waste,
                           total_users=total_users,
                           collection_spots=collection_spots,
                           e_waste_items=e_waste_items)


@app.route('/pricing')
@login_required
def pricing_page():
    e_waste_items = get_e_waste_items()  # Fetch data from your database
    return render_template('pricing.html', e_waste_items=e_waste_items)


collection_Ispots = [
    {"name": "Spot 1", "latitude": 28.7041, "longitude": 77.1025, "address": "Delhi"},
    {"name": "Spot 2", "latitude": 19.0760, "longitude": 72.8777, "address": "Mumbai"},
    {"name": "Spot 3", "latitude": 12.9716, "longitude": 77.5946, "address": "Bangalore"},
]


@app.route('/spots')
@login_required
def spots():
    return render_template('spots.html')


@app.route('/get_collection_spots')
@login_required
def get_collection_spots_json():
    return jsonify(collection_Ispots)


if __name__ == '__main__':
    app.run(debug=True)
