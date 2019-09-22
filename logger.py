import logging

logging_config = logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(funcName)s():%(lineno)d - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)