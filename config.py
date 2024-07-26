
import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@db:5432/sensor_data' #Configuração do banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'b96a6afebaa48b0b1a482561f1f9c32e8dc4e7f5b4e85ad8' #Uma Hash aleatória que eu fiz
    API_KEY = os.getenv('API_KEY', '12345678909876543210') #Uma api key aleatória que criei simplesmente um vai e vem dos numeros ahsuahsuashu