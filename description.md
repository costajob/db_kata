# Summary
Please complete the below Python Question and send your response back to us within the next week (by 18 September). Please use just the Python standard library and do let me know if you have any specific queries around the test itself:

The coding challenge is to create a small and simple database-like program. The challenge consists of four tasks. You are neither required nor expected to complete all four tasks. You should complete enough tasks as to provide a small sample of the level and style of your coding ability. Generally, completing task 1 and 2.1 should be sufficient.

## Importer and Datastore
You will be provided with a pipe separated file in the following format.

### File Sample:

```txt
PROJECT|SHOT|VERSION|STATUS|FINISH_DATE|INTERNAL_BID|CREATED_DATE
the hobbit|1|64|scheduled|2010-05-15|45.00|2010-04-01 13:35
lotr|3|16|finished|2001-05-15|15.00|2001-04-01 06:47
king kong|42|128|scheduled|2006-07-22|45.00|2006-08-04 07:22
the hobbit|40|32|finished|2010-05-15|22.80|2010-03-22 01:10
king kong|42|128|not required|2006-07-22|30.00|2006-10-15 09:14
```

### Field Descriptions:
* PROJECT: The project name or code name of the shot. (Text, max size 64 char)
* SHOT: The name of the shot. (Text, max size 64 char)
* VERSION: The current version of the file. (Integer, between 0 and 65535 inclusive)
* STATUS: The current status of the shot. (Text, max size 32 char)
* FINISH_DATE: The date the work on the shot is scheduled to end. (Date in YYYY-MM-DD format)
* INTERNAL_BID: The amount of days we estimate the work on this shot will take. (Floating-point number, between 0 and 65535)
* CREATED_DATE: The time and date when this record is being added to the system. (Timestamp in YYYY-MM-DD HH:MM format)

### Task
Your first task is to parse and import the file into a simple datastore. You may use any file format that you want to implement to store the data. Records in the datastore should be unique by PROJECT, SHOT and VERSION. Subsequent imports with the same logical record should overwrite the earlier records.



## Query tool

### select, order and filter
The next task is to create a query tool that can execute simple queries against the datastore you created in step one. The tool should accept command line args for SELECT, ORDER and FILTER functions:

```shell
$ ./query -s PROJECT,SHOT,VERSION,STATUS -o FINISH_DATE,INTERNAL_BID
lotr,3,16,finished
king kong,42,128,not required
the hobbit,40,32,finished
the hobbit,1,64,scheduled
```

```shell
$ ./query -s PROJECT,SHOT,VERSION,STATUS -f FINISH_DATE=2006-07-22
king kong,42,128,not required
```

### group and aggregate functions
The next step is to add group by and aggregate functions to your query tool.  Your tool should support the following aggregates:
* MIN: select the minimum value from a column
* MAX: select the maximum value from a column
* SUM: select the summation of all values in a column (Only supported for number types)
* COUNT: count the distinct values in a column
* COLLECT: collect the distinct values in a column

```shell
$ ./query -s PROJECT,INTERNAL_BID:sum,SHOT:collect -g PROJECT
the hobbit,67.00,[1,40]
lotr,15.00,[3]
king kong,30.00,[42]
```

### advanced filter function
Add a filter function which evaluates boolean AND and OR expressions in the following format:

```
PROJECT="the hobbit" AND SHOT=1 OR SHOT=40
```

Assume AND has higher precedence than OR. Parentheses can be added to change the above statement to the more logical:

```
PROJECT="the hobbit" AND (SHOT=1 OR SHOT=40)
```

#### Example:
```shell
$ ./query -s PROJECT,INTERNAL_BID -f 'PROJECT="the hobbit" OR PROJECT="lotr"'
the hobbit,45.00
lotr,15.00
the hobbit,22.80
```
