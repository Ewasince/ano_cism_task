import logging as log
import threading
import time
from typing import Never

import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from config import config
from message_broker.dto.task import Task, StatusTask, StatusEnum


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


def publish(channel: BlockingChannel, data: bytes, properties):
    channel.basic_publish(
        exchange='',
        routing_key=config.broker_channel_tasks,
        body=data,
        properties=properties,
    )
    pass


def start_publishing(rmq_parameters, delay: int = 3, priority: int = 10, name: str = 'publisher'):
    with BlockingConnection(rmq_parameters) as rmq_connection:
        rmq_channel = rmq_connection.channel()

        rmq_channel.queue_declare(queue=config.broker_channel_tasks, arguments={"x-max-priority": 50})

        basic_prop = pika.BasicProperties(priority=priority)

        while True:
            task_local_count = get_task_num()
            task = Task(task_number=task_local_count)

            data = bytes(task.model_dump_json(), 'utf-8')
            publish(rmq_channel, data, basic_prop)

            log.info(f'[{name}] message = {task_local_count} published!')

            log.debug(f'[{name}] wait before new message')
            time.sleep(delay)
            pass
    pass


def callback(ch, method, properties, body: bytes):
    received_task = StatusTask.model_validate_json(body)

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


def callback_opened(ch, method, properties, task: StatusTask):
    log.debug(f'[publisher] {task=} opened has been processed')
    pass


def callback_in_progress(ch, method, properties, task: StatusTask):
    log.debug(f'[publisher] {task=} in_progress has been processed')
    pass


def callback_closed(ch, method, properties, task: StatusTask):
    log.info(f'[publisher] {task=} closed has been processed')
    pass


def callback_exception(arg: Never, *args):
    raise Exception('Unknown status type')
    pass


def listen_completed_tasks(rmq_parameters):
    connection = pika.BlockingConnection(rmq_parameters)
    channel = connection.channel()

    channel.queue_declare(queue=config.broker_channel_completed)

    channel.basic_consume(queue=config.broker_channel_completed, on_message_callback=callback, auto_ack=True)

    log.info(f'[publisher] Waiting for complete tasks\' messages')
    channel.start_consuming()
    pass
