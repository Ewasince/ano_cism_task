import logging as log
import time
import sys

from pika import PlainCredentials, ConnectionParameters, BlockingConnection

from config import config
from message_broker.dto.task import TaskStatus, Task, StatusEnum

rmq_parameters = ConnectionParameters(
    host=config.broker_host,
    port=config.broker_port,
    credentials=PlainCredentials(
        username=config.broker_username,
        password=config.broker_password,
    )
)


def start_listen():
    connection = BlockingConnection(rmq_parameters)
    channel = connection.channel()

    channel.queue_declare(queue=config.broker_channel_tasks, arguments={"x-max-priority": 50})
    channel.queue_declare(queue=config.broker_channel_completed)

    def send_task_status(task: TaskStatus):
        channel.basic_publish(
            exchange='',
            routing_key=config.broker_channel_completed,
            body=bytes(task.model_dump_json(), 'utf-8'),
        )
        log.debug(f'[consumer] ack sent')
        pass

    def callback(ch, method, properties, body: bytes):
        received_task: Task = Task.model_validate_json(body)

        start_time = time.time()

        time.sleep(0.1)
        task_status = TaskStatus(task_number=received_task.task_number, elapsed_time=time.time() - start_time)
        log.info(f"[consumer] Opened {task_status=}.")
        send_task_status(task_status)

        time.sleep(0.1)
        task_status.status = StatusEnum.IN_PROGRESS
        task_status.elapsed_time = time.time() - start_time
        log.info(f"[consumer] Processed {task_status=}.")
        send_task_status(task_status)

        time.sleep(0.1)
        task_status.status = StatusEnum.CLOSED
        task_status.elapsed_time = time.time() - start_time
        log.info(f"[consumer] Closed {task_status=}.")
        send_task_status(task_status)

        pass

    channel.basic_consume(
        queue=config.broker_channel_tasks,
        on_message_callback=callback,
        auto_ack=True
    )

    # print(' [*] Waiting for messages. To exit press CTRL+C')
    log.info('[consumer] Waiting for messages')
    channel.start_consuming()


if __name__ == '__main__':
    logging = log
    log = logging.getLogger('consumer')
    log.setLevel(logging.DEBUG)
    format = logging.Formatter(
        '%(filename)17s[LINE:%(lineno)3d]# %(levelname)-6s [%(asctime)s]  %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(format)
    console_handler.setLevel(config.log_level_console)
    log.addHandler(console_handler)

    start_listen()
    pass
