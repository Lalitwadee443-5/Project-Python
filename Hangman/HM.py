import random
import sqlite3

conn=sqlite3.connect('hm.db')
cur=conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Users
    (id INTEGER PRIMARY KEY AUTOINCREMENT , Name TEXT UNIQUE, Score REAL)''')

def get_number_of_attempts():#เดากี่รอบ
    while True:
        attempts=input('How many wrong attempts do you want? Choose from 1 to 20.\n')
        try:
            attempts=int(attempts)
            if 0<attempts<21:
                print('Okay!')
                return(attempts)
            else:
                print('Sorry, you cannot use this.')
        except:
            print('Sorry, you cannot use this.')

def get_word_length():#จำนวนตัวอักษรของคำศัพท์
    while True:
        length=input('How long a word are you willing to try? Choose from 4 to 11.\n')
        try:
            length=int(length)
            if (3<length<12):
                print('Okay')
                return(length)
            else:
                print('You have not put a valid number.')
        except:
            print('You have not put a valid number.')

def playgame():#login&playgame
    score=0
    while True:#ถามข้อมูลเพื่อที่จะบันทึกลงในตารางuser
        new_old=input('Are you a new user?\n')
        username=input('What is your name?\n').capitalize()#ให้ตัวแรกของชื่อเป็นตัวพิมพ์ใหญ่
        if new_old.lower() in ['yes','y','ya']:
            try:
                cur.execute('INSERT INTO Users(Name,Score) VALUES(?,?)',(username,0.0))
                break
            except:
                print('You cannot choose this id. Please choose a different one.')
                continue
        elif new_old.lower() in ['no','n','na']:
            try:
                cur.execute('SELECT Name FROM Users WHERE Name=? ',(username,))
                current_user=cur.fetchone()[0]
                break
            except:
                print('This user does not exist.')
                continue
        else:
            print('Please give a valid reply.')
            continue

    print('''\nYour score will be calculated in the game. For higher score choose less number of attempts and try to use minimum in each round.''')
    print('''Note: No score is awarded if you don't win.\n''')

    while True:
        print('\n***Let us play hangman!***\n')

        #userกรอกข้อมูล

        attempts=get_number_of_attempts()
        original_attempts=attempts

        length=get_word_length()

        print('''
        ***Getting Word***
            \n''')

        #เปิดไฟล์คำศัพท์
        fh= open('wordlist.txt','r')
        wordlist=fh.read().split()

        #แรนด้อมคำศัพท์
        while True:
            cur.execute('''SELECT word FROM hangman WHERE length=? ORDER BY RANDOM() ''',(length,))
            user_word=cur.fetchone()[0]
            #print(user_word)

            #ให้คำใบ้
            cur.execute('SELECT meaning FROM hangman WHERE word=?',(user_word,))
            try:
                hint=cur.fetchone()[0]
            except:
                continue
            if hint is None: continue

            if user_word in hint and ':' in hint or ':' in hint:
                hint=hint.split(':')[0]
                break
            elif user_word in hint:
                continue
            else:
                break

        #ถามuserว่าอยากได้คำใบ้ไหม
        while True:
            ask_for_hint=input('Do you want a hint?\n')
            if ask_for_hint in ['yes','Y','YES','Yes','y']:
                break
            elif ask_for_hint in ['N','NO','no','n','No']:
                break
            else:
                print('Please put a valid reply.')
                continue

        #Main Game
        show_word='*'*length
        guess_list=list()
        while True:
            if attempts==0: #ถ้าattemptsครบจะจบลูป
                print('You have used all of your attempts. Your word was: '+user_word)
                break
            if ask_for_hint in ['yes','Y','YES','Yes','y']:
                print('Hint: '+hint)
            print('Word: '+show_word)
            print('Number of wrong attempts remaining:'+str(attempts))
            while True:
                guess=input('Guess letter(s):')
                if guess=='quit()':break
                if guess=='':continue
                else:break
            if guess=='quit()':break
            guess=guess.lower()
            user_word=user_word.lower()
            print('\n')


            #แจ้งให้userรู้ว่า เคยเดาคำนี้ไปแล้ว
            if guess in guess_list:
                print('You have already used this before.')
                print('Guessed items include:',guess_list)
                continue
            else:
                guess_list.append(guess)

            #การทำรายการตำแหน่งของตัวอักษรที่เดาสำหรับการเดาครั้งเดียวหรือหลายครั้ง
            indices=list()
            if guess in user_word:
                print('Your guess was right!\n')
                for ind,letter in enumerate(user_word):
                    if guess==letter:
                        indices.append(ind)
                if len(indices)>1:
                    for ind in indices:
                        show_word=show_word[:ind]+guess+show_word[ind+1:] #อัปเดตคำที่โชว์user
                else:
                    guess_index=user_word.index(guess)
                    #อัปเดตคำที่โชว์user
                    show_word=show_word[:guess_index]+guess+show_word[guess_index+len(guess):]

                if '*' not in show_word: #ถ้าuserเดาถูกหมดให้แสดงข้อความ
                    print('Congratulations! You have won this round!\n')
                    print('Your word was: '+show_word)
                    current_score=20-original_attempts+(attempts/2)
                    score=20-original_attempts+(attempts/2)+score
                    print('Your score for this round is: '+str(current_score))
                    print('Your total score is: '+str(score))
                    break
            else: #ถ้าuserยังเดาไม่ถูกให้แสดงข้อความ
                print('Sorry, your guess was wrong.\n')
                attempts=attempts-1

        #ถามuserว่าจะเล่นต่อไหม
        while True:
            askagain=input('Do you want to play again (Y/N)?\n')
            if askagain.lower() in ['yes','ya','y']:
                print('Okay! Let us start again\n')
                break
            elif askagain.lower() in ['na','no','n']:

                #อัปเดตคะแนนuserก่อนออก
                cur.execute('SELECT Score FROM Users WHERE Name=?',(username,))
                prev_score=cur.fetchone()[0]

                if score > prev_score:
                    print('\nYou have a new high score!\n')
                    cur.execute('''UPDATE Users SET Score=? WHERE Name=?''',(score,username))
                    print('Your previous high score was: '+str(prev_score))
                    print('Your new high score is: '+str(score))
                else:
                    print("\nYou don't have a new high score, your current high score stays at:",prev_score)


                conn.commit()
                go()
            else:
                print('Please type a valid reply.')
                continue

        continue

def sc():#ดูคะแนน
    while True:
        username=input('What is your name?\n').capitalize()
        try:
            cur.execute('SELECT Score FROM Users WHERE Name=?',(username,))
            current_user=cur.fetchone()
            print('Your Score is ',current_user)
            print('\n')
            break
        except:
            print('You are a new player! Plese login.')
            continue

def go():#เล่นเกม
    while True:
        print('\n-----HANGMAN GAME-----\nPlay Game ---- press 1\nView Score --- press 2\nExit --------- press 3\n')
        a=int(input('What do you want to do ? : '))
        if a==1:
            playgame()
        elif a==2:
            sc()
        elif a==3:
            print('Good Bye! See you soon.')
            quit()
        else:
            print('ERROR! Plese press only 1,2,3')
            break

while True:#main
    go()