import logging
import os.path
import sys
import time
from logging import handlers
from multiprocessing import Process

import pika
from pika.credentials import PlainCredentials

from config import config

log = logging.getLogger('publisher')
log.setLevel(logging.DEBUG)
format = logging.Formatter(
    '%(filename)17s[LINE:%(lineno)3d]# %(levelname)-6s [%(asctime)s]  %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(format)
console_handler.setLevel(config.log_level_console)
log.addHandler(console_handler)

if not os.path.exists(config.log_file):
    with open(config.log_file, 'w') as f:
        f.write('')
        pass
    pass

file_handler = handlers.TimedRotatingFileHandler(
    config.log_file,
    when='midnight',
    backupCount=config.keep_log_files,
    encoding=None,
    delay=False,
    utc=True)
file_handler.setFormatter(format)
file_handler.setLevel(config.log_level_file)
log.addHandler(file_handler)

rmq_parameters = pika.ConnectionParameters(
    host=config.broker_host,
    port=config.broker_port,
    credentials=PlainCredentials(
        username=config.broker_username,
        password=config.broker_password,
    )
)


def start_publishing():
    with pika.BlockingConnection(rmq_parameters) as rmq_connection:
        rmq_channel = rmq_connection.channel()

        rmq_channel.queue_declare(queue=config.broker_channel_tasks)

        basic_prop = pika.BasicProperties(priority=10)

        counter = 0
        while True:
            # rmq_channel.basic_publish(exchange='',
            #                           routing_key='test_key',
            #                           body=bytes(f'test message {counter}!', 'utf-8'),
            #                           properties=basic_prop)

            message = f'[publisher] Fictive message №{counter}'

            ## noinspection PyTypeChecker
            rmq_channel.basic_publish(
                exchange='',
                routing_key=config.broker_channel_tasks,
                body=bytes(message, 'utf-8'),
                properties=basic_prop,
            )
            log.info(f'[publisher] message = {message} published!')

            counter += 1
            log.debug(f'[publisher] wait before new message')
            time.sleep(3)
            pass
    pass


def listen_completed_tasks():
    connection = pika.BlockingConnection(rmq_parameters)
    channel = connection.channel()

    channel.queue_declare(queue=config.broker_channel_completed)

    def callback(ch, method, properties, body: bytes):
        received_message = str(body, 'utf-8')
        log.info(f'[publisher] {received_message=} has been processed')
        pass

    channel.basic_consume(queue=config.broker_channel_completed, on_message_callback=callback, auto_ack=True)

    log.info(f'[publisher] Waiting for complete tasks\' messages')
    channel.start_consuming()
    pass


if __name__ == '__main__':
    # publisher = Process(target=start_publishing, name='Main task publisher')
    # publisher.start()

    checker = Process(target=listen_completed_tasks, name='Complete task checker')
    checker.start()

    #

    start_publishing()
    pass
