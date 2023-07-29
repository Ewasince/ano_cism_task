import datetime
import json
import logging
import os
import sys
import time
from logging import handlers
from math import ceil
from multiprocessing import Process

# import schedule
# from alembic.runtime.migration import MigrationContext
# from flask import Flask, request, render_template, redirect, url_for
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask_swagger_ui import get_swaggerui_blueprint
from flask import render_template, request  # Remove: import Flask
# import connexion
from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from api.dto.user_creds import UserCreds
from service.config import *
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


# app = Flask(__name__)
# CORS(app)


# class InputSchema(Schema):
#     number = fields.Int(description="Число", required=True, example=5)
#     power = fields.Int(description="Степень", required=True, example=2)
#
#
# class OutputSchema(Schema):
#     result = fields.Int(description="Результат", required=True, example=25)
#
#
# class ErrorSchema(Schema):
#     result = fields.String(description="Ошибка", required=True, example='ok')
#
#
# def create_tags(spec):
#     """ Создаем теги.
#
#     :param spec: Объект APISpec для сохранения тегов
#     """
#     tags = [{'name': 'math', 'description': 'Математические функции'}]
#
#     for tag in tags:
#         print(f"Добавляем тег: {tag['name']}")
#         spec.tag(tag)
#
#
# def load_docstrings(spec, app):
#     """ Загружаем описание API.
#
#     :param spec: объект APISpec, куда загружаем описание функций
#     :param app: экземпляр Flask приложения, откуда берем описание функций
#     """
#     for fn_name in app.view_functions:
#         if fn_name == 'static':
#             continue
#         print(f'Загружаем описание для функции: {fn_name}')
#         view_fn = app.view_functions[fn_name]
#         spec.path(view=view_fn)
#
#
# def get_apispec(app):
#     """ Формируем объект APISpec.
#
#     :param app: объект Flask приложения
#     """
#     spec = APISpec(
#         title="My App",
#         version="1.0.0",
#         openapi_version="3.0.3",
#         plugins=[FlaskPlugin(), MarshmallowPlugin()],
#     )
#
#     spec.components.schema("Input", schema=InputSchema)
#     spec.components.schema("Output", schema=OutputSchema)
#     spec.components.schema("Error", schema=ErrorSchema)
#
#     create_tags(spec)
#
#     load_docstrings(spec, app)
#
#     return spec
#
#
# SWAGGER_URL = '/docs'
# API_URL = '/swagger'
#
# swagger_ui_blueprint = get_swaggerui_blueprint(
#    SWAGGER_URL,
#    API_URL,
#    config={
#        'app_name': 'My App'
#    }
# )
#
# app.register_blueprint(swagger_ui_blueprint)


# def job_learn_if_learning_day():
#     if datetime.date.today().day == 1 or datetime.date.today().day == 15:
#         datetime_now = datetime.datetime.now()
#         analytics.learn_all(datetime_now)
#
#
# def job_check_deviations():
#     cur_datetime = datetime.datetime.now()
#     analytics.check_deviations_all(cur_datetime)
#     pass
#
#
# def run():
#     try:
#         # schedule.every().day.at('01:00').do(job_learn_if_learning_day)
#         # schedule.every().day.at('00:00').do(job_check_deviations)
#         schedule.run_all()
#         while True:
#             schedule.run_pending()
#             time.sleep(1)
#     except Exception as e:
#         log.error(f'JOB: [SCHEDULER] [FAIL] runtime error, scheduler halt. error: {e}')
#         exit(1)  # will not actually terminate process but rest status should become 'False'
#     finally:
#         # TODO stop all jobs
#         pass

@app.route("/spec")
def spec():
    return jsonify(swagger(app))


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
          id: User
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
    res = await users_api.authentication(user_creds)

    if res:
        return 'ok',  200
    else:
        return 'incorrect login or password', 400
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

    res = await users_api.list_users()

    if res:
        return json.dumps(res), 200
    else:
        return 'ok', 400
    pass
