from bs4 import BeautifulSoup #ดึงข้อมูลหน้าเว็บ
import urllib.request, urllib.parse, urllib.error #เข้าถึงอินเทอร์เน็ต
from urllib.parse import urljoin 
import ssl
import re
import sqlite3

#ละเว้นข้อผิดพลาดใบรับรอง SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh=open('wordlist.txt','r')
wordlist=fh.read().split()

conn=sqlite3.connect('hm.db')
cur=conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS hangman
    (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT UNIQUE, meaning TEXT)''')

for word in wordlist:

    cur.execute('SELECT word FROM hangman WHERE word==?',(word,))
    box=cur.fetchone()
    if box is None:
        print('Not Found!')
    else:
        print('Found!')
        continue
    try:
        fhand=urllib.request.urlopen('https://www.dictionary.com/browse/'+word,context=ctx)
    except:
        continue
    html=fhand.read()
    soup=BeautifulSoup(html,'html.parser')
    meta_tag=soup.find_all('meta')
    definition=meta_tag[1].get('content')
    meaning=re.findall('definition,(.*)\. S',definition)
    if len(meaning)<1:continue

    meaning=meaning[0].split(';')[0] #แบ่งคำ
    print(meaning)

    cur.execute('INSERT OR IGNORE INTO hangman(word,meaning) VALUES(?,?)',(word,meaning.strip())) #แยกwordกับmeaningออกจากกัน
    conn.commit()
    print('done')
