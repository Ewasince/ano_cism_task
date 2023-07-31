import json

from flask import request
from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from api.dto.user_creds import UserCreds
import service.api.user_api as users_api

SWAGGER_URL = ''
API_URL = '/spec'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'My App'
    }
)

app = Flask(__name__)
app.register_blueprint(swagger_ui_blueprint)


@app.route("/spec")
def spec():
    return jsonify(swagger(app))


@app.route("/test", methods=['GET'])
def test():
    return 'Hello, World!'


@app.route('/api/registration', methods=['POST'])
async def registration():
    """
    Register a new user
    ---
    tags:
      - users
    parameters:
      - in: body
        name: body
        schema:
          id: UserCreds
          required:
            - login
            - password
          properties:
            login:
              type: string
              description: логин пользователя
              example: adminlogin
            password:
              type: string
              description: пароль пользователя
              example: qwerty123
    produces:
      - application/json
    responses:
      '200':
        description: Successful response
      '400':
        description: Bad Request
      '500':
        description: Internal Server Error
    """

    response_data = json.loads(request.data)
    user_creds = UserCreds(**response_data)

    try:
        await users_api.registration(user_creds)
        return 'ok', 200
    except Exception as e:
        return str(e), 500

    pass


@app.route('/api/authentication', methods=['POST'])
async def authentication():
    """
    Login existing user
    ---
    tags:
      - users
    parameters:
      - in: body
        name: body
        schema:
          id: UserCreds
          required:
            - login
            - password
          properties:
            login:
              type: string
              description: логин пользователя
              example: adminlogin
            password:
              type: string
              description: пароль пользователя
              example: qwerty123
    produces:
      - application/json
    responses:
        '200':
          description: Successful response
          content:  # Response body
            type: str
            example: ok
        '400':
          description: Bad Request
          content:  # Response body
            type: str
            example: incorrect login or password
        '500':
          description: Internal Server Error
    """

    response_data = json.loads(request.data)
    user_creds = UserCreds(**response_data)

    try:
        res = await users_api.authentication(user_creds)

        if res:
            return 'ok', 200
        else:
            return 'incorrect login or password', 400
    except Exception as e:
        return str(e), 500
    pass


@app.route('/api/list_users', methods=['POST'])
async def list_users():
    """
    List existing users
    ---
    tags:
      - users
    produces:
      - application/json
    responses:
      '200':
        description: Successful response
        schema:
          type: string
          example: ["user_a", "user_b"]
      '400':
        description: Bad Request
      '500':
        description: Internal Server Error
    """
    try:
        res: dict | list = await users_api.list_users()

        return json.dumps(res), 200
    except Exception as e:
        return str(e), 500
    pass

print('TESTTESTTEST')
