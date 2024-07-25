from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import os
import csv
from io import StringIO

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<SensorReading {self.equipment_id} {self.timestamp} {self.value}>"

db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/sensor_data', methods=['POST'])
@login_required
def receive_sensor_data():
    data = request.get_json()
    equipment_id = data.get('equipmentId')
    timestamp = datetime.fromisoformat(data.get('timestamp'))
    value = data.get('value')

    new_reading = SensorReading(equipment_id=equipment_id, timestamp=timestamp, value=value)
    db.session.add(new_reading)
    db.session.commit()

    return jsonify({"message": "Sensor data salvo com sucesso"}), 201

@app.route('/upload_csv', methods=['POST'])
@login_required
def upload_csv():
    file = request.files['file']
    stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    
    for row in csv_input:
        equipment_id = row[0]
        timestamp = datetime.fromisoformat(row[1])
        value = float(row[2])
        
        new_reading = SensorReading(equipment_id=equipment_id, timestamp=timestamp, value=value)
        db.session.add(new_reading)
    
    db.session.commit()
    return jsonify({"message": "CSV data salvo com sucesso"}), 201

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/average/<period>')
@login_required
def get_average(period):
    if period not in ['24h', '48h', '1w', '1m']:
        return jsonify({"error": "Invalid period"}), 400

    now = datetime.now()
    if period == '24h':
        start_time = now - timedelta(hours=24)
    elif period == '48h':
        start_time = now - timedelta(hours(48))
    elif period == '1w':
        start_time = now - timedelta(weeks(1))
    elif period == '1m':
        start_time = now - timedelta(days(30))

    results = db.session.query(SensorReading.equipment_id, db.func.avg(SensorReading.value)).filter(
        SensorReading.timestamp >= start_time
    ).group_by(SensorReading.equipment_id).all()

    return jsonify({equipment_id: avg for equipment_id, avg in results})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
