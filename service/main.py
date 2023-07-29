import logging
import sys
from logging import handlers

from api.rest import app
# from api.rest import app
from config import config
# from service.api.rest import app

log = logging.getLogger('')
log.setLevel(logging.DEBUG)
format = logging.Formatter(
    '%(filename)17s[LINE:%(lineno)3d]# %(levelname)-6s [%(asctime)s]  %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(format)
console_handler.setLevel(config.log_level_console)
log.addHandler(console_handler)

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


    # check and init DATABASE
    # log.debug(f"[STARTUP] [DATABASE] [START] Database version start")
    try:
        # engine = create_engine(os.getenv('DATABASE_URL', 'driver://user:pass@localhost/dbname'))
        # conn = engine.connect()
        # context = MigrationContext.configure(conn, opts={
        #     'version_table_schema': ALEMBIC_VERSION_TABLE_SCHEMA})
        # current_rev = context.get_current_revision()

        # log.debug(f'[{method_prefix}] [DATABASE] Database version: revision= {current_rev}')

        log.info(f'Приложение запущено с параметрами: \n{config.model_dump()}')
        # start()
        app.run(host=config.service_host, port=config.service_port)
    except Exception as e:
        log.critical(f'Critical fail: {e}')
    log.info('### STOP ###')