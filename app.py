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

# Model do usuario, definindo as variáveis relacionadas às colunas da tabela user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Model do sensor, definindo as variáveis relacionadas às colunas da tabela sensor_reading
class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<SensorReading {self.equipment_id} {self.timestamp} {self.value}>"
    
# Método de verificação da chave da api, para que haja uma certa segurança de que os dados enviados são confiáveis
def verify_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key') or request.args.get('api_key') or request.json.get('api_key')
        if api_key != app.config['API_KEY']:
            return jsonify({"error": "API key Inválida"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Rota só pra caso não seja especificado qual rota
@app.route('/')
def index():
    return redirect(url_for('login'))

# Rota para registrar novo usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário resgistrado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Rota de login
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
            flash('Falha no login. Por favor, cheque seu usuario e senha', 'danger')
    return render_template('login.html')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rota de cadastro das informações que retornam dos equipamentos
@app.route('/sensor_data', methods=['POST'])
@verify_api_key
def receive_sensor_data():
    data = request.get_json()
    equipment_id = data.get('equipmentId')
    timestamp = datetime.fromisoformat(data.get('timestamp'))
    value = data.get('value')

    new_reading = SensorReading(equipment_id=equipment_id, timestamp=timestamp, value=value)
    db.session.add(new_reading)
    db.session.commit()

    return jsonify({"message": "Sensor data salvo com sucesso"}), 201

# Rota de upload do arquivo e inserção ou atualização dos dados com base no .csv
@app.route('/upload_csv', methods=['POST'])
@verify_api_key
def upload_csv():
    # Verifica se foi passado um arquivo realmente
    if 'file' not in request.files:
        return jsonify({"error": "Sem arquivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    
    # Ignora a primeira linha, pois contém o cabeçalho
    next(csv_input, None)
    
    rows_processed = 0
    for row in csv_input:
        # Verifica se o arquivo csv possui menos do que 3 colunas, caso sim, invalido
        if len(row) < 3:
            return jsonify({"error": "Arquivo em formato invalido"}), 400

        equipment_id = row[0]
        timestamp = datetime.fromisoformat(row[1])
        value = float(row[2])

        # Verifica se já existe um registro com o mesmo equipment_id e timestamp
        existing_reading = SensorReading.query.filter_by(equipment_id=equipment_id, timestamp=timestamp).first()
        
        if existing_reading:
            # Atualiza o valor do registro existente
            existing_reading.value = value
        else:
            # Cria um novo registro
            new_reading = SensorReading(equipment_id=equipment_id, timestamp=timestamp, value=value)
            db.session.add(new_reading)
        rows_processed += 1
    
    db.session.commit()
    return jsonify({"message": f"{rows_processed} linhas processadas e salvas com sucesso."}), 201


#Rota que carrega a página de dashboard que contém o gráfico das médias dos periodos
@app.route('/dashboard')
@login_required
def dashboard():
    api_key = app.config['API_KEY']
    return render_template('dashboard.html', api_key=api_key)

#Rota para buscar a média do periodo selecionado ordenando pelo id do equipamento
@app.route('/api/average/<period>')
@login_required
def get_average(period):
    if period not in ['24h', '48h', '1s', '1m']:
        return jsonify({"error": "Periodo inválido"}), 400

    now = datetime.now()
    if period == '24h':
        start_time = now - timedelta(hours=24)
    elif period == '48h':
        start_time = now - timedelta(hours=48)
    elif period == '1s':
        start_time = now - timedelta(weeks=1)
    elif period == '1m':
        start_time = now - timedelta(days=30)

    results = db.session.query(SensorReading.equipment_id, db.func.avg(SensorReading.value)).filter(
        SensorReading.timestamp >= start_time
    ).group_by(SensorReading.equipment_id).all()

    return jsonify({equipment_id: avg for equipment_id, avg in results})

if __name__ == "__main__":
    from seed import seed_data
    db.create_all()
    seed_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
