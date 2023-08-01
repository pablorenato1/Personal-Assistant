from queue import Queue
import logging

shared_queue = Queue()
shared_speech_queue = Queue(maxsize=2)

logging.basicConfig(level=logging.DEBUG, filename='log.log', filemode='a', format="%(asctime)s - %(levelname)s - %(message)s")

# Set debug files
info_logger = logging.getLogger('info_logger')
debug_logger = logging.getLogger('debug_logger')
error_logger = logging.getLogger('error_logger')

# Set/Create logger file
info_handler = logging.FileHandler('info_log_file.log')
debug_handler = logging.FileHandler('debug_log_file.log')
error_handler = logging.FileHandler('error_log_file.log')

# Set level of each handler
info_handler.setLevel(logging.INFO)
debug_handler.setLevel(logging.DEBUG)
error_handler.setLevel(logging.WARNING)

# Set the style of logging
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

info_logger.addHandler(info_handler)
debug_logger.addHandler(debug_handler)
error_logger.addHandler(error_handler)