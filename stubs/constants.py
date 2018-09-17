from weta_db.datastore import Column, Table
from weta_db.importer import Parser
from weta_db.values import DateVal, FloatVal, IntVal, TimeVal, TxtVal

project = Column('PROJECT', TxtVal(), True, desc='the project name or code name of the shot')
shot    = Column('SHOT', TxtVal(), True, desc='the name of the shot')
version = Column('VERSION', IntVal(), True, desc='the current version of the file')
status  = Column('STATUS', TxtVal(_max=32), desc='the current status of the shot')
finish  = Column('FINISH_DATE', DateVal(), desc='the date the work on the shot is scheduled to end')
bid     = Column('INTERNAL_BID', FloatVal(), desc='the amount of days we estimate the work on this shot will take')
created = Column('CREATED_DATE', TimeVal(), desc='the time and date when this record is being added to the system')
COLUMNS = (project, shot, version, status, finish, bid, created)
ROWS    = list(Parser('./stubs/sample.txt'))
SHUFFLE = list(Parser('./stubs/shuffled.txt'))
TABLE   = Table.factory(ROWS, COLUMNS)
