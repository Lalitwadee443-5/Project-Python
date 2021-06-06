import sqlite3

conn=sqlite3.connect('hm.db')
cur=conn.cursor()

try:
    cur.execute('''ALTER TABLE hangman
        ADD length NULL''')

    fh=open('wordlist.txt','r')
    wordlist=fh.read().split()

    for word in wordlist:
        word_length=len(word)
        cur.execute('''UPDATE hangman
            SET length=? WHERE word=?''',(word_length,word))

except:
    print('Something is not right')
    quit()

conn.commit()
