#!/usr/bin/python
from sys import argv
import psycopg2
import re

nargs = len(argv)

if (nargs>2):
    print 'multiple words detected, only the first word is used'
    word = argv[1]
    uword = re.sub('\'',' ', word)
elif (nargs==2):
    word=argv[1]
    uword = re.sub('\'',' ', word)


conn = psycopg2.connect(database="tcount", user="postgres",
                        password="pass", host="localhost", port="5432")

#get cursor
cur = conn.cursor()
if 'uword' in globals():
    cur.execute("SELECT word, count FROM tweetwordcount where word='%s'" %(uword))
    result = cur.fetchone()
    if result:
        print ("Total number of '%s': %s " %(result[0],result[1]))
    else:
        print ("Total number of  '%s' : %s" %(uword, 0))
else:
    cur.execute("SELECT word, count FROM tweetwordcount order by word asc")
    allresults = cur.fetchall()
    for item in allresults:
        print ("Frequency of %s: %s," %(item[0], item[1]))

conn.commit()

conn.close()
