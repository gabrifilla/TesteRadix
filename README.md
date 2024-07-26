# API Sensor Data

## Configuração

1. Clone o repositório
2. Navegue até a pasta do repositório clonado
3. Rode o comando `docker compose up -d --build`
4. Acesse a API em `http://localhost:5000`

Ao fazer a inicialização do projeto, conta padrão de acesso será criada:

username: admin
senha: admin

e

username: user
senha: user

*Necessário fazer login para entrar na dashboard, onde o gráfico fica.* *

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


## Testes
Dentro do projeto instalei uma biblioteca chamada locust, que, pelo que eu entendi, manipula as requisições, podendo enviar mais de uma ao emsmo tempo, as vezs até várias por segundo.

Para acessar o locust e realizar os testes, basta se direcionar para a página em `http://localhost:8089`

Em seguida, preencha os campos conforme necessário, por exemplo:

Number of users: 500 (quantas requisições vão ser feitas)
Ramp up: 10 (de quanto em quanto segundos as requisições vão ser feitas)

Assim que tiver preenchido os campos, basta clicar em Start.

## Outros
Dentro da pasta "outros", na raiz do projeto, adicionei o arquivo .csv com o formato que eu consegui fazer o código identificar. (tentei fazer com arquivos excel, mas não deu certo, não reconhecia de jeito nenhum, unico que funcionou foi o formato que está na pasta realmente)

**Payload exemplo:**
```json
{
  "equipmentId": "EQ-12495",
  "timestamp": "2023-02-15T01:30:00.000-05:00",
  "value": 78.42
}
