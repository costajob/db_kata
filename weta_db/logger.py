'''
Synopsis
--------
The logger singleton for the main program, tracing to ERROR level by default.
'''

import logging
from os import path

FILENAME = path.abspath('./weta_db.log')
FORMAT = '[%(asctime)s #%(process)d] -- %(levelname)s : %(message)s'
logging.basicConfig(filename=FILENAME, format=FORMAT, level=logging.ERROR)
BASE = logging.getLogger(__name__)
