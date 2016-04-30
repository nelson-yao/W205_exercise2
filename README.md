# W205_exercise2

### Getting the Files
use the following way to clone the respository
```
git clone https://github.com/seriousNel/W205_exercise2.git
```
### Database setup 

After starting the instance, using the pre-baked instance for exercise 2. Make sure postgres is installed.
Start postgres and build the database using the following code

```
psql -U postgres
CREATE DATABASE tcount;
\c tcount;
CREATE TABLE tweetwordcount (word TEXT PRIMARY KEY   NOT NULL, count INT NOT NULL);
\q
```
### make streamparse project 
```
sparse quickstart wordcount
```

### Streaming and analysis

To start running the streaming, use:
```
cd wordcount
sparse run
```
After allowing enough time passes, stop streaming by Ctrl+D
To query the occurence of the a certain word:
```
python finalresults.py yes
```
To see the occurence of all the words:

```
python finalresults.py
```
To get tuples of words that have frequency between k1 and k2: 

```
python histogram.py k1 k2
```










