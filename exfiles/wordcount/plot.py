from sys import argv
import psycopg2


def plot():
    conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
    cur=conn.cursor()

    cur.execute("""SELECT * FROM tweetwordcount ORDER BY count desc LIMIT 21""")
    result=cur.fetchall()

    labels=[]
    values=[]
    for item in result:
        labels.append(item[0])
        values.append(str(item[1]))

    results=[labels, values]

    with open("top20.txt", "w" ) as outfile:
        for label, value in zip(labels, values):
            outfile.write(",".join([label, value]))
            outfile.write("\n")

    outfile.close()




if __name__=="__main__":
    plot()
