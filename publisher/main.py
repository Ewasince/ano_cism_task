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
from message_broker.dto.task import StatusTask, StatusEnum, Task
from publisher import start_publishing, listen_completed_tasks

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

if __name__ == '__main__':
    publisher = Thread(target=start_publishing,
                       kwargs={'rmq_parameters': rmq_parameters, 'delay': 2, 'priority': 10, 'name': 'pub10'})
    publisher.start()

    publisher = Thread(target=start_publishing,
                       kwargs={'rmq_parameters': rmq_parameters, 'delay': 4, 'priority': 20, 'name': 'pub20'})
    publisher.start()

    # checker = Process(target=listen_completed_tasks, name='Complete task checker')
    # checker.start()

    #

    # start_publishing()

    listen_completed_tasks(rmq_parameters)
    pass
