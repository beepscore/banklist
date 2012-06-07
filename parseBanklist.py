#!/usr/bin/python

import sqlite3;
from datetime import datetime, date;

# References:
# http://www.raywenderlich.com/902/sqlite-101-for-iphone-developers-creating-and-scripting
# https://explore.data.gov/Banking-Finance-and-Insurance/FDIC-Failed-Bank-List/pwaj-zn2n

conn = sqlite3.connect('banklist.sqlite3')
c = conn.cursor()
c.execute('drop table if exists failed_banks')
# Note tutorial doesn't have acquiring_institution, and uses zip instead of cert_number.
# Maybe the government changed the csv file.
# generate a unique key named 'id'
c.execute('create table failed_banks(id integer primary key autoincrement, bank_name text, city text, state text, cert_number integer, acquiring_institution text, closing_date text, updated_date text)')

# returns an array of elements that were preiously separated by commas
# ignores commas within quotes
def mysplit (string):
    quote = False
    retval = []
    current = ""
    for char in string:
        if char == '"':
            #toggle quote
            quote = not quote
        elif char == ',' and not quote:
            #comma is not within quotes so it is a delimiter
            retval.append(current)
            current = ""
        else:
            current += char

    retval.append(current)
    return retval

# Read lines from file, skipping first line
data = open("banklist.csv", "r").readlines()[1:]
for entry in data:
    # Parse values
    vals = mysplit(entry.strip())
    # Convert dates to sqlite3 standard format
    # closing_date
    vals[5] = datetime.strptime(vals[5], "%d-%b-%y")
    # updated_date
    vals[6] = datetime.strptime(vals[6], "%d-%b-%y")
    # Insert row into table
    print "Inserting %s..." % (vals[0])
    # sql command. Pass NULL so SQLite will generate an id
    sql = "insert into failed_banks values(NULL, ?, ?, ?, ?, ?, ?, ?)"
    c.execute(sql, vals)

# Done
conn.commit()

# Get failed banks by year, for fun
c.execute("select strftime('%Y', closing_date), count(*) from failed_banks group by 1;")
years = []
failed_banks = []
for row in c:
    years.append(row[0])
    failed_banks.append(row[1])
 
# Plot the data, for fun
import matplotlib.pyplot as plt
import numpy.numarray as na
 
values = tuple(failed_banks)
ind = na.array(range(len(values))) + 0.5
width = 0.35
plt.bar(ind, values, width, color='r')
plt.ylabel('Number of failed banks')
plt.title('Failed banks by year')
plt.xticks(ind+width/2, tuple(years))
plt.show()

