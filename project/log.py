################################################################################
# Social Buzz Clustering
# - Logger -
#
# Author <a href='mailto:wei.tah.chai@sap.com'>Chai Wei Tah</a>
# Copyright (C) 2015 by MLI SG SAP Inc.
################################################################################

# -- Load library --
import logging

__copyright__ = "Copyright (C) 2015 MLI SG SAP Inc."
__license__ = "MLI SG SAP"
__version__ = "0.1.0"


#  -- custom logger --
def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    # handler = logging.StreamHandler()
    handler = logging.FileHandler('logs/application.log')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger
