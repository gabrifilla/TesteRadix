from locust import HttpUser, TaskSet, task, between
import random
from datetime import datetime

class SensorTasks(TaskSet):
    equipment_counter = 0 #Inicia o contador
    @task
    def post_sensor_data(self):
      # Incrementa o contador
      self.equipment_counter += 1
      equipment_id = f"EQ-{12498 + self.equipment_counter}"

      timestamp = datetime.now().isoformat()

      value = round(random.uniform(1000.00, 9999.99), 2)

      # Define o cabeçalho com a chave de API
      headers = {'x-api-key': '12345678909876543210'}
      
      # Define o envio json para a rota /sensor_data
      self.client.post("/sensor_data", json={
          "equipmentId": equipment_id,
          "timestamp": timestamp,
          "value": value
      }, headers=headers)

class SensorUser(HttpUser):
    tasks = [SensorTasks]
    wait_time = between(1, 5)
