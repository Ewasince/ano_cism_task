import logging
import os.path
import sys
import threading
import time
from logging import handlers
from multiprocessing import Process
from threading import Thread
from typing import Never

import pika
from pika.credentials import PlainCredentials

from config import config
from message_broker.dto.task import TaskStatus, StatusEnum, Task

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


def get_task_num_func():
    task_count = 0
    task_count_lock = threading.Lock()

    def wrapped() -> int:
        nonlocal task_count_lock
        nonlocal task_count

        with task_count_lock:
            value = task_count
            task_count += 1
            return value
        pass

    return wrapped


get_task_num = get_task_num_func()


def start_publishing(delay: int = 3, priority: int = 10, name: str = 'publisher'):

    with pika.BlockingConnection(rmq_parameters) as rmq_connection:
        rmq_channel = rmq_connection.channel()

        rmq_channel.queue_declare(queue=config.broker_channel_tasks, arguments={"x-max-priority": 50})

        basic_prop = pika.BasicProperties(priority=priority)

        while True:
            task_local_count = get_task_num()
            task = Task(task_number=task_local_count)

            rmq_channel.basic_publish(
                exchange='',
                routing_key=config.broker_channel_tasks,
                body=bytes(task.model_dump_json(), 'utf-8'),
                properties=basic_prop,
            )
            log.info(f'[{name}] message = {task_local_count} published!')

            log.debug(f'[{name}] wait before new message')
            time.sleep(delay)
            pass
    pass


def listen_completed_tasks():
    connection = pika.BlockingConnection(rmq_parameters)
    channel = connection.channel()

    channel.queue_declare(queue=config.broker_channel_completed)

    def callback(ch, method, properties, body: bytes):
        received_task = TaskStatus.model_validate_json(body)

        match received_task.status:
            case StatusEnum.OPENED:
                process_callback = callback_opened
            case StatusEnum.IN_PROGRESS:
                process_callback = callback_in_progress
            case StatusEnum.CLOSED:
                process_callback = callback_closed
            case _:
                process_callback = callback_exception
        process_callback(ch, method, properties, received_task)
        # received_message = str(body, 'utf-8')
        pass

    def callback_opened(ch, method, properties, task: TaskStatus):
        log.debug(f'[publisher] {task=} opened has been processed')
        pass

    def callback_in_progress(ch, method, properties, task: TaskStatus):
        log.debug(f'[publisher] {task=} in_progress has been processed')
        pass

    def callback_closed(ch, method, properties, task: TaskStatus):
        log.info(f'[publisher] {task=} closed has been processed')
        pass

    def callback_exception(arg: Never, *args):
        raise Exception('Unknown status type')
        pass

    channel.basic_consume(queue=config.broker_channel_completed, on_message_callback=callback, auto_ack=True)

    log.info(f'[publisher] Waiting for complete tasks\' messages')
    channel.start_consuming()
    pass


if __name__ == '__main__':
    publisher = Thread(target=start_publishing, kwargs={'delay': 2, 'priority': 10, 'name': 'pub10'})
    publisher.start()

    publisher = Thread(target=start_publishing, kwargs={'delay': 4, 'priority': 20, 'name': 'pub20'})
    publisher.start()

    # checker = Process(target=listen_completed_tasks, name='Complete task checker')
    # checker.start()

    #

    # start_publishing()

    listen_completed_tasks()
    pass
