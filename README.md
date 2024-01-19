**README.md**

# Credit Card API

## Sumário

- [Objetivos](#objetivos)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Utilização](#utilização)
- [Docker](#docker)


## Objetivos
O objectivo desta api é realizar o cadastro e a consulta de dados de cartão de crédito. Para tanto foi-se utilizado um sistem para criptografia de descriptografia destes dados por se tratar de dados sensíveis.

## Requisitos

Certifique-se de ter o Python instalado com uma versão maior que 3.8. Você pode instalar os requisitos executando:

```bash
   pip install -r requirements.txt
```

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/josejonatasoliveira/credit_card_api.git
   ```

2. Acesse o diretório do projeto:

   ```bash
   cd credit_card_api
   ```
3. Crie um ambiente virtual:
    ```bash
   python -m venv .env
   ```

    Ative o ambiente virtual

   ```bash
   .env\\Scripts\\activate.bat
   ```

4. Instale os requisitos:

   ```bash
   pip install -r requirements.txt
   ```

5. Migre as tabelas padrões do Django

   ```bash
   python manage.py migrate

6. Rodar
Após os passos anteriores esta na hora de rodar a api, para isso bastar executar o seguinte comando.
    ```bash
   python manage.py runserver 8040
   ```

## Utilização

Antes de poder utilizar a api é necessário que seja criado um usuário para que seja feita autenticação nos endpoints utilizados. Para criar um usuário vá até o endpoit `POST /users/` e preencha as informações necessárias.

![User POST](https://github.com/josejonatasoliveira/credit_card_api/blob/master/images/user_post.png)

Após a criação do usuário será possivel a cria um `JWT` para fazer requisição nas apis.
Para criar um `JWT` basta enviar o username e o password para api `auth/jwt/create`. Será retornado um json parecido com este.
   ```bash
      {
         "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNTc1NzEwMCwiaWF0IjoxNzA1NjcwNzAwLCJqdGkiOiI1YzU1MTI2ZmZmMTg0YmNjYjA2OGM1MWY5OGI0YjEwZCIsInVzZXJfaWQiOjF9.9oj8Ki4FDNZ4JK3z3QDFSMv-3JkyV9wRDSNyS2Ph6Z4",
         "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1Njc0MzAwLCJpYXQiOjE3MDU2NzA3MDAsImp0aSI6ImFhMjQ2Mzc4MjBlYTRhNTY5NjI2NzY2YTg5ZDlkYjRkIiwidXNlcl9pZCI6MX0.jEAePfJi_4zPi0Kh6Wa9IF3v5FQGVkOPxCUZ05beLqI"
      }
   ```

Agora podemos criar os dados do cartão de crédito encriptados, para isso faça uso da api teste `/encrypt-credit-card`.
![Encrypt Credit Card](https://github.com/josejonatasoliveira/credit_card_api/blob/master/images/encrypt_credit_card.png)

Com os dados do cartão de crédito encriptados basta agora usar api a `cards` para salva-lo.
![Encrypt Credit Card](https://github.com/josejonatasoliveira/credit_card_api/blob/master/images/jwt_uses.png)

##  Docker
Para instalar via docker basta executar o seguinte comando dentro da pasta `credit_card_api`.

```bash
   docker-compose up --build
```

Após a execução destes comandos a api estará rodando na porta 8040 do localhost.
http://localhost:8040