from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2
import re

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()
        conn = psycopg2.connect(user="postgres", password="pass", host="localhost", port="5432")
        cur = conn.cursor()
        #conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        #cur.execute("""DROP DATABASE IF EXISTS tcount""")

        #cur.execute("""CREATE DATABASE tcount""")

        #cur.execute("""CREATE TABLE tweetwordcount (word TEXT PRIMARY KEY   NOT NULL, count INT NOT NULL)""")
        conn.commit()


    def process(self, tup):
        word = tup.values[0]
        ### espace the apostrophe

        uWord=word.replace("\'", " ")

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount
        # Table name: Tweetwordcount
        # you need to create both the database and the table in advance.

        conn = psycopg2.connect(database="tcount", user="postgres", password="password", host="localhost", port="5432")
        cur = conn.cursor()
        
        #cur.execute("""SELECT COUNT(*) from tweetwordcount WHERE word=\'{}\'""" .format(uWord))
        if uWord in self.counts:
            try:
                cur.execute("""UPDATE tweetwordcount SET count=%s WHERE word=%s;""",(self.counts[uWord], uWord))
                self.counts[uWord] += 1
                conn.commit()
            except:
                self.log('could not insert')
        else:
            try:
                cur.execute("""INSERT INTO tweetwordcount (word,count) VALUES (%s, %s);""" , (uWord,1))
                self.counts[uWord]=1
                conn.commit()
            except:
                self.log('could not update')

        self.emit([uWord, self.counts[uWord]])

        # Log the count - just to see the topology running
        self.log('%s: %s' %(uWord, self.counts[uWord]))
