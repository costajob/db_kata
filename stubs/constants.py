import datastore as ds
import importer as im
import values as v

project = ds.Column('PROJECT', v.TxtVal(), True, desc='the project name or code name of the shot')
shot    = ds.Column('SHOT', v.TxtVal(), True, desc='the name of the shot')
version = ds.Column('VERSION', v.IntVal(), True, desc='the current version of the file')
status  = ds.Column('STATUS', v.TxtVal(_max=32), desc='the current status of the shot')
finish  = ds.Column('FINISH_DATE', v.DateVal(), desc='the date the work on the shot is scheduled to end')
bid     = ds.Column('INTERNAL_BID', v.FloatVal(), desc='the amount of days we estimate the work on this shot will take')
created = ds.Column('CREATED_DATE', v.TimeVal(), desc='the time and date when this record is being added to the system')
COLUMNS = (project, shot, version, status, finish, bid, created)
TABLE   = ds.Table(COLUMNS)
ROWS    = list(im.Parser('./stubs/sample.txt'))
SHUFFLE = list(im.Parser('./stubs/shuffled.txt'))
