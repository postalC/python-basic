################################################################################
# Social Buzz Clustering
# -  ML Classification Module -
#
# Author <a href='mailto:wei.tah.chai@sap.com'>Chai Wei Tah</a>
# Copyright (C) 2015 by MLI SG SAP Inc.
################################################################################
# -- Load library --
from flask import json
from classification import predictNew
from classification import loadClassifier
from database import db, Data
from sqlalchemy.orm import sessionmaker
import logging

__copyright__ = "Copyright (C) 2015 MLI SG SAP Inc."
__license__ = "MLI SG SAP"
__version__ = "0.1.0"

# -- Logger --
logger = logging.getLogger('root')

# -- Load classifier from model file --
__clf = loadClassifier('model/clf.pkl')
__groups = {'positive': 0, 'negative': 1, 'neutral': 2, 'question': 3}

# -- Database Session --
Session = sessionmaker(bind=db)
session = Session()


# -- Return Single Classification --
def getClassify(__id, __message):
    try:
        __msgList = [__message]
        __predict = predictNew(__clf, __msgList, __groups)
        logger.debug("Predictions on new comments: ")
        logger.debug("--------------------------------------------------------------")
        logger.debug("Input Messages: %s ==> %s", __msgList[0], __predict[0])
        logger.debug("--------------------------------------------------------------")
        __model = Data(__id, __msgList[0], __predict[0])
        session.add(__model)
        session.commit()
        __data = {
            'id': __id,
            'result': __predict[0]
        }
        return __data
    except (ValueError, KeyError, TypeError):
        logger.error("Exception: %s, %s, %s", ValueError, KeyError, TypeError)
        session.rollback()


# -- Return Bulk Classification --
def getClassifies(__messages):
    try:
        __json = json.loads(__messages)
        __idList = list()
        __msgList = list()
        for x in __json['messages']:
            __idList.append(x['id'])
            __msgList.append(x['message'])

        __response = list()
        __predict = predictNew(__clf, __msgList, __groups)
        logger.debug("Predictions on new comments: ")
        logger.debug("--------------------------------------------------------------")
        for i in range(len(__msgList)):
            __response.append({'id': __idList[i], 'result': __predict[i]})
            __model = Data(__idList[i], __msgList[i], __predict[i])
            session.add(__model)
            logger.debug("Input Messages: %s ==> %s", __msgList[i], __predict[i])
        logger.debug("--------------------------------------------------------------")
        session.commit()

        __data = {
            'results': __response
        }
        return __data
    except (ValueError, KeyError, TypeError):
        logger.error("Exception: %s, %s, %s", ValueError, KeyError, TypeError)
        session.rollback()
