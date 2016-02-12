################################################################################
# Social Buzz Clustering
# -  SqlAlchemy Database -
#
# Author <a href='mailto:wei.tah.chai@sap.com'>Chai Wei Tah</a>
# Copyright (C) 2015 by MLI SG SAP Inc.
################################################################################
# -- Load library --
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

__copyright__ = "Copyright (C) 2015 MLI SG SAP Inc."
__license__ = "MLI SG SAP"
__version__ = "0.1.0"

# -- Database --
Base = declarative_base()


# -- SBC table --
class Data(Base):
    __tablename__ = 'sbc'

    id = Column(Integer, primary_key=True)
    c4cid = Column(String(40), nullable=False)
    message = Column(String(5000), nullable=False)
    classified = Column(String(20), nullable=False)

    def __init__(self, c4cid=None, message=None, classified=None):
        self.c4cid = c4cid
        self.message = message
        self.classified = classified

    def __repr__(self):
        return "Data(%r, %r, %r)" % (self.c4cid, self.message, self.classified)


db = create_engine('sqlite:///db//sbuzz.db')
Base.metadata.create_all(db, checkfirst=True)
