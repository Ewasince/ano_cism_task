import logging as log
import time
import sys

from pika import PlainCredentials, ConnectionParameters, BlockingConnection

from config import config

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

    channel.queue_declare(queue=config.broker_channel_tasks)
    channel.queue_declare(queue=config.broker_channel_completed)

    def callback(ch, method, properties, body: bytes):
        received_message = str(body, 'utf-8')
        log.info(f"[consumer] Received {received_message}. Will complete in 2 seconds...")
        time.sleep(2)
        log.info(f"[consumer] {received_message} completed!")

        message_ack = f'{received_message} completed!'

        # noinspection PyTypeChecker
        channel.basic_publish(
            exchange='',
            routing_key=config.broker_channel_completed,
            body=bytes(message_ack, 'utf-8'),
        )
        log.debug(f'[consumer] ack sent')
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
