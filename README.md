# API Sensor Data
<sub><sup>Adendo: É a primeira vez que desenvolvo em python sem que seja pra coisas futeis (tipo buscar botão na tela e clicar quando tiver alteração)</sup></sub>

### Tópicos 

:small_blue_diamond: [Descrição do projeto](#descrição-do-projeto)

:small_blue_diamond: [Funcionalidades](#funcionalidades)

:small_blue_diamond: [Endpoints](#endpoints)

:small_blue_diamond: [Pré-requisitos](#pré-requisitos)

:small_blue_diamond: [Como rodar a aplicação](#configuração)

:small_blue_diamond: [Testes](#testes)

:small_blue_diamond: [Outros](#outros)

## Descrição do projeto

<p align="justify">
  Este projeto é uma aplicação para monitorar e armazenar dados de sensores em tempo real, utilizando Flask, SQLAlchemy e Bootstrap. A aplicação também permite o upload de arquivos CSV para inserir dados em massa e fornece uma interface de dashboard com gráficos para a visualização dos dados.
</p>

## Funcionalidades
- Recebimento de dados de equipamentos sensores via API.
- Upload de dados via arquivos CSV.
- Visualização de dados em uma dashboard.
- Autenticação e autorização, tanto de login quanto de envio das informações através do equipamento.

## Pré-requisitos
:warning: [Python](https://www.python.org/downloads/release/python-3124/)

## Configuração

1. No terminal, clone o repositório: 
  ```
  git clone https://github.com/gabrifilla/TesteRadix.git
  ```
2. Navegue até a pasta do repositório clonado
  ```
  cd ./TesteRadix
  ```
3. Rode o comando de inicialização
  ```
  docker compose up -d --build
  ```
4. Acesse a aplicação em `http://localhost:5000`

Ao fazer a inicialização do projeto, conta padrão de acesso será criada:

username: admin
senha: admin

e

username: user
senha: user

*Necessário fazer login para entrar na dashboard, onde o gráfico fica.* *

## Endpoints

### `GET e POST /login`
Envia e recebe as informações do usuário e carrega a página de dashboard caso sucesso.

### `/logout`
Desconecta o usuário, fazendo retornar para a página de login.

### `GET e POST /register`
Recebe as informações de cadastro de usuário e faz o cadastro.

### `/dashboard`
Página inicial com as informações de média do periodo selecionado e o gráfico de apresentação.

### `POST /sensor_data`
Recebe as informações em tempo real.

**Payload exemplo:**
```json
{
  "equipmentId": "EQ-12495",
  "timestamp": "2023-02-15T01:30:00.000-05:00",
  "value": 78.42
}
```

### `POST /upload_csv`
Recebe o arquivo csv para preencher os dados.

### `GET /api/average/<period>`
Busca as informações no banco de acordo com a data especificada e faz a média com base no retorno.

## Testes
Dentro do projeto instalei uma biblioteca chamada locust, que, pelo que eu entendi, manipula as requisições, podendo enviar mais de uma ao emsmo tempo, as vezs até várias por segundo.

Para acessar o locust e realizar os testes, basta se direcionar para a página em `http://localhost:8089`

Em seguida, preencha os campos conforme necessário, por exemplo:

Number of users: 500 (quantas requisições vão ser feitas)
Ramp up: 10 (de quanto em quanto segundos as requisições vão ser feitas)

Assim que tiver preenchido os campos, basta clicar em Start.

## Outros
Dentro da pasta "outros", na raiz do projeto, adicionei o arquivo .csv com o formato que eu consegui fazer o código identificar. (tentei fazer com arquivos excel, mas não deu certo, não reconhecia de jeito nenhum, unico que funcionou foi o formato que está na pasta realmente)