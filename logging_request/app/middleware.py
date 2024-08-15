import time
import traceback

from .logger.logger import Logger

logger = Logger()


class LoggingDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log_file_name = request.user.username if request.user.is_authenticated else request.META['REMOTE_ADDR']

        logger.info(f'Метод запроса - [{request.method}]', log_file_name=log_file_name)
        logger.info(f'URL запроса - [{request.path}]',  log_file_name=log_file_name)
        logger.info(f'IP запроса - [{request.META['REMOTE_ADDR']}]',  log_file_name=log_file_name)
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        logger.info(f'Время запроса - [{(end_time - start_time)}ms]',  log_file_name=log_file_name)
        logger.line(log_file_name=log_file_name)
        return response

    def process_exception(self, request, exception, *args, **kwargs):
        log_file_name = request.user.username if request.user.is_authenticated else request.META['REMOTE_ADDR']
        logger.error(traceback.format_exc(), log_file_name=log_file_name)
        logger.line(log_file_name=log_file_name)
