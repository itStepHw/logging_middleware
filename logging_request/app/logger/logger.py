import inspect
import os
import threading

from datetime import datetime
from .config import DELIMITER, CURRENT_PATH


class Logger:
    _lock = threading.Lock()
    # _instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
    #     return cls._instance

    def __init__(self, log_file_name: str = ''):
        date = datetime.now().strftime('%d_%m_%Y')
        self.__log_file_name = f"log_{date}" if len(log_file_name) <= 0 else f"{log_file_name}_{date}"
        self.__message = '',
        self.__date_time = datetime.now()
        self.__file_name = inspect.stack()[1].filename

        self.__logger_enable: bool = False
        self.__info_enable: bool = False
        self.__debug_enable: bool = False
        self.__error_enable: bool = False
        self.__warning_enable: bool = False
        self.__print_enable: bool = False
        self.__line_enable: bool = True
        self.__success_enable: bool = False
        self.__start_enable: bool = False

        self.__config_file_read()

    @staticmethod
    def __create_directory_if_not_exists(dir_path: str):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def __config_file_create():
        file = 'logger.conf'
        if not os.path.isfile(f'{CURRENT_PATH}{DELIMITER}{file}'):
            with open(f'{CURRENT_PATH}{DELIMITER}{file}', 'a', encoding='utf-8') as conf:
                conf.write(f"#logger_enable=True\n")
                conf.write(f"#info_enable=True\n")
                conf.write(f"#debug_enable=False\n")
                conf.write(f"#error_enable=True\n")
                conf.write(f"#warning_enable=True\n")
                conf.write(f"#print_enable=True\n")
                conf.write(f"#line_enable=False\n")
                conf.write(f"#success_enable=True\n")
                conf.write(f"#start_enable=True\n")
                conf.close()

    def __config_file_read(self):
        self.__config_file_create()
        with open(f'{CURRENT_PATH}{DELIMITER}logger.conf', 'r', encoding='utf-8') as conf:
            lines = conf.readlines()
            for line in lines:
                if line.startswith('#'):
                    rest_of_string = line[1:-1:]
                    key, value = rest_of_string.split('=')

                    if key == 'logger_enable':
                        self.__logger_enable = True if value.strip() == 'True' else False
                    elif key == 'info_enable':
                        self.__info_enable = True if value.strip() == 'True' else False
                    elif key == 'debug_enable':
                        self.__debug_enable = True if value.strip() == 'True' else False
                    elif key == 'error_enable':
                        self.__error_enable = True if value.strip() == 'True' else False
                    elif key == 'warning_enable':
                        self.__warning_enable = True if value.strip() == 'True' else False
                    elif key == 'print_enable':
                        self.__print_enable = True if value.strip() == 'True' else False
                    elif key == 'line_enable':
                        self.__line_enable = True if value.strip() == 'True' else False
                    elif key == 'success_enable':
                        self.__success_enable = True if value.strip() == 'True' else False
                    elif key == 'start_enable':
                        self.__start_enable = True if value.strip() == 'True' else False

    @staticmethod
    def __add_empty(log_type) -> str:
        if log_type == 'INFO':
            return ' ' * 3
        if log_type == 'OK':
            return ' ' * 5
        if log_type != 'WARNING':
            return ' ' * 2
        else:
            return ''

    def __write(self, log_type: str, to_console: bool, log_file_name: str):
        if self.__logger_enable:
            self.__create_directory_if_not_exists(f'{CURRENT_PATH}{DELIMITER}log')

            log_entry = f"[{log_type}]{self.__add_empty(log_type)} [{self.__date_time}] - {self.__message}"

            with open(f'{CURRENT_PATH}{DELIMITER}log{DELIMITER}{self.__log_file_name if not log_file_name else log_file_name}.log', 'a',
                      encoding='utf-8') as file:
                file.write(log_entry + '\n')

            if self.__print_enable and to_console:
                print(f'{log_entry}')

    def debug(self, message: str, to_console: bool = True, log_file_name: str = None):
        if self.__debug_enable:
            self.__message = message
            self.__write(f'DEBUG', to_console, log_file_name)

    def info(self, message: str, to_console: bool = True, log_file_name: str = None):
        if self.__info_enable:
            self.__message = message
            self.__write(f'INFO', to_console, log_file_name)

    def error(self, message: str, to_console: bool = True, log_file_name: str = None):
        if self.__error_enable:
            self.__message = message
            self.__write(f'ERROR', to_console, log_file_name)

    def warning(self, message: str, to_console: bool = True, log_file_name: str = None):
        if self.__warning_enable:
            self.__message = message
            self.__write(f'WARNING', to_console, log_file_name)

    def line(self, message: str = None, to_console: bool = True, log_file_name: str = None):
        if message is None:
            self.__message = f'-' * 20
        else:
            self.__message = f'-' * 20 + message
        self.__write(f'INFO', to_console, log_file_name)

    def succes(self, message: str, to_console: bool = True, log_file_name: str = None):
        if self.__success_enable:
            self.__message = message
            self.__write(f'OK', to_console, log_file_name)

    def start(self, message: str, to_console: bool = True, log_file_name: str = None):
        if self.__start_enable:
            self.__message = message
            self.__write(f'START', to_console, log_file_name)
