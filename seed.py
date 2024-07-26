from app import db, User, SensorReading
from flask_bcrypt import generate_password_hash
from datetime import datetime

def seed_data():
    # Checa se existe usuários cadastrados na tabela
    if User.query.first() is None:
        # Se não existir, cria os dois usuários padrões
        user1 = User(username='admin', password=generate_password_hash('admin').decode('utf-8'))
        user2 = User(username='user', password=generate_password_hash('user').decode('utf-8'))

        # Adiciona eles na sessão que vai fazer o envio das informações pro banco
        db.session.add(user1)
        db.session.add(user2)

    # Repete o que aconteceu acima, mas com sensor agora
    if SensorReading.query.first() is None:
        
        sensor_readings = [
            SensorReading(equipment_id='EQ-12495', timestamp=datetime(2023, 2, 15, 1, 30), value=78.42),
            SensorReading(equipment_id='EQ-12496', timestamp=datetime(2023, 2, 16, 2, 45), value=82.56),
            SensorReading(equipment_id='EQ-12497', timestamp=datetime(2023, 2, 17, 3, 15), value=76.89),
        ]

        
        db.session.add_all(sensor_readings)

    # Envia a sessão para que o SQLAlchemy faça o cadastro no banco.
    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    seed_data()
    print('Database seeded successfully')
