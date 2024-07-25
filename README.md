# API Sensor Data

## Configuração

1. Clone o repositório
2. Navegue até a pasta do repositório clonado
3. Rode o comando `docker compose up -d --no-deps --build`
4. Acesse a API em `http://localhost:5000`

## Endpoints

### `GET e POST /login`
Envia as informações do usuário e envia para a página de dashboard caso sucesso.

### `/dashboard`
Página inicial com as informações de média do periodo selecionado.

### `/logout`
Desconecta o usuário, fazendo retornar para a página de login.

### `GET e POST /register`
Recebe as informações de usuário.

### `POST /sensor_data`
Recebe as informações em tempo real.

### `POST /upload_csv`
Recebe o arquivo csv para preencher os dados.

### `GET /api/average/<period>`
Recebe o arquivo csv para preencher os dados.

**Payload:**
```json
{
  "equipmentId": "EQ-12495",
  "timestamp": "2023-02-15T01:30:00.000-05:00",
  "value": 78.42
}
