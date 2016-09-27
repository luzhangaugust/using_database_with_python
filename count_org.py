
'''
Author: Lu Zhang
Language: Python and SQL
Date: September 27, 2016
Code: create db, create table (org, count) and count number emails per organization
Note: week 2 assessment from the Coursera MOOC Using Databases with Python
'''


import sqlite3

conn = sqlite3.connect('orgdb.sqlite') #make connection with database
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')         #drop exsiting TABLE

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''') #recreate the table

fname = raw_input('Enter file name: ')                #it pause and wait for the file name I wanted to work with
if ( len(fname) < 1 ) : fname = 'mbox.txt'
fh = open(fname)

email = []
for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split()
    email.append(pieces[1])
    part = [i.split('@')[1] for i in email]
    org = part[-1]
    #print email
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES ( ?, 1 )''', ( org, ) )
    else :
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?',
            (org, ))
    # This statement commits outstanding changes to disk each
    # time through the loop - the program can be made faster
    # by moving the commit so it runs only after the loop completes
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

print
print "Counts:"
for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

cur.close()
