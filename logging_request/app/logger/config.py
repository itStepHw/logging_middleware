import os
import sys

DELIMITER = '\\' if os.name == 'nt' else '/'
CURRENT_PATH = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
MODULE_PATH = '../../../../../Desktop/modules'
CSV_FILES = '_csv_files'