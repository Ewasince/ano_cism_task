import logging
import os
import sys
from logging import handlers
from multiprocessing import Process
from threading import Thread

from api.rest import app
from config import config
from message_broker.consumer import start_listen

log = logging.getLogger('')
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
    backupCount=int(config.keep_log_files),
    encoding=None,
    delay=False,
    utc=True)
file_handler.setFormatter(format)
file_handler.setLevel(config.log_level_file)
log.addHandler(file_handler)

if __name__ == '__main__':
    log.info('### START ###')

    try:
        log.info(f'Приложение запущено с параметрами: \n{config.model_dump()}')

        checker = Thread(target=start_listen, name='Complete task checker')
        checker.start()
        log.info(f'Потребитель сообщений запущен')

        app.run(host=config.service_host, port=config.service_port)
    except Exception as e:
        log.critical(f'Critical fail: {e}')
        os._exit(1)
    log.info('### STOP ###')
