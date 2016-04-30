from sys import argv
import psycopg2

def histogram(k1, k2):
    conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
    cur=conn.cursor()
    try:
        cur.execute("SELECT * FROM tweetwordcount where count BETWEEN %s and %s order by count desc" %(int(k1), int(k2)-1))
        conn.commit()
        result=cur.fetchall()
        for item in result:
            print str(item[0])+": "+ str(item[1])
        return result

    except ValueError:
        print("Invalid input, please enter two integers")


if __name__=="__main__":
    if len(argv)==3:
        histogram(argv[1], argv[2])
    else:
        print("Please input exactly two numbers")
