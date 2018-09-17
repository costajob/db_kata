# Table of Contents

* [Scope](#scope)
* [Python](#python)
* [Design](#design)
* [APIs](#apis)
* [Tests](#tests)

## Scope
This program is the implementation of the [Weta Digital](https://www.wetafx.co.nz/) kata for the Python Senior developer position.

## Python
The program works with Python versions equal or greater than 3.3 (since the `yield from` construct is used on the `query` module).  
The program has no external dependencies from the available standard library (as requested).  
This program has been tested with the following Python's versions:

* 3.3.1  

* 3.4.8  

* 3.6.4  

* 3.7.0  

## Design
The program has been implemented by following the single responsibility principle of object oriented design: every modules contains single classes that try to do just one thing right.

### Modules
The program has the following first level modules:  

* `values`: contains the value-objects used to represent column values and responsible to validate valid range and cast to properly type (i.e. date, time, float, int, string)   

* `datastore`: contains the core logic related to data organization, such as columns information and the table object representing grouped data  

* `importer`: contains the parsing logic and the storage (read/write) based on the `pickle` serialization module (a whole `datastore.Table` object is serialized)  

* `query`: contains the core logic used by the CLI API to select, group, filter and sort stored data  

## APIs
The application exposes a single CLI interface via the Python's `argparse` module.  
The `query` API is used to select, group, filter and order data from the specified source (default to `stubs/projects.pickle`):

```shell
$ ./query -h
usage: query [-h] [-d DATASTORE] [-s SELECT] [-g GROUP] [-f FILTER] [-o ORDER]

Select, group, filter and order data from the specified datastore

optional arguments:
  -h, --help            show this help message and exit
  -d DATASTORE, --datastore DATASTORE
                        the path of the datastore file to select data from
  -s SELECT, --select SELECT
                        select just specified column names, separated by
                        comma, optionally prefixed by colon and aggregate name
  -g GROUP, --group GROUP
                        group data by specified column name, combined by
                        aggregates on select clause
  -f FILTER, --filter FILTER
                        filter column by specified value
  -o ORDER, --order ORDER
                        sort data by specified column names, separated by
                        comma
```

### Examples

#### Select all
```shell
$ ./query
the hobbit,1,64,scheduled,2010-05-15,45.0,2010-04-01 13:35
lotr,3,16,finished,2001-05-15,15.0,2001-04-01 06:47
king kong,42,128,not required,2006-07-22,30.0,2006-10-15 09:14
the hobbit,40,32,finished,2010-05-15,22.8,2010-03-22 01:10
```

#### Select and order
```shell
$ ./query -s PROJECT,SHOT,VERSION,STATUS,FINISH_DATE -o FINISH_DATE,INTERNAL_BID
lotr,3,16,finished,2001-05-15
king kong,42,128,not required,2006-07-22
the hobbit,40,32,finished,2010-05-15
the hobbit,1,64,scheduled,2010-05-15
```

#### Select and group
```shell
$ ./query -s PROJECT,VERSION:max,INTERNAL_BID:sum,SHOT:collect,STATUS:count -g PROJECT
the hobbit,64,67.8,[1,40],2
lotr,16,15.0,[3],1
king kong,128,30.0,[42],1
```

#### Select and filter
```shell
$ ./query -s PROJECT,INTERNAL_BID,VERSION -f 'PROJECT="the hobbit" AND (SHOT=1 OR SHOT=40)'
the hobbit,45.0,64
the hobbit,22.8,32
```

#### Combine all
```shell
$ ./query -s PROJECT,VERSION:max,INTERNAL_BID:sum,SHOT:collect,FINISH_DATE -g PROJECT -f 'PROJECT="the hobbit" OR PROJECT="lotr"' -o FINISH_DATE
lotr,16,15.0,[3],2001-05-15
the hobbit,64,67.8,[1,40],2010-05-15
```

## Tests
The whole program is covered by fast, isolated unit tests by using the standard `unittest` module.  

A single executable will run all of the available unit tests:
```shell
./run_tests
```
