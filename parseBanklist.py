import sqlite3;
from datetime import datetime, date;

conn = sqlite3.connect('banklist.sqlite3')
c = conn.cursor()
c.execute('drop table if exists failed_banks')
#generate a unique key named 'id'
c.execute('create table failed_banks(id integer primary key autoincrement, name text, city text, state text, zip integer, close_date text, updated_date text)')
