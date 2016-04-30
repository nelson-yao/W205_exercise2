from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2
import re

conn = psycopg2.connect(database="tcount", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()

counts = Counter()

uWord="blahre3"
counts[uWord]=+1


cur.execute("""INSERT INTO tweetwordcount (word,count) VALUES (%s, %s);""" , (uWord,1))

counts[uWord] += 1

conn.commit()
