from datetime import datetime
import sqlite3
from Decrypt import Decrypt
from sqlite3.dbapi2 import connect


class sqlitedb:
    def __init__(self,name):
        name=f"vaults/{name}"
        self.conn = sqlite3.connect(name,check_same_thread=False)
        self.c = self.conn.cursor()
 
    def readfromdb(self):
        conn = self.conn
        c = self.c
        c.execute("SELECT name,username,password FROM passwords")
        data = c.fetchall()
        conn.close()
        return data

    def readfromnotes(self):
        conn = self.conn
        c = self.c
        c.execute("SELECT title,note FROM notes")
        data = c.fetchall()
        conn.close()
        return data
    def readfromcards(self):
        conn = self.conn
        c = self.c
        c.execute("SELECT name,number,security_code FROM cards")
        data = c.fetchall()
        conn.close()
        return data
        
class writetodb:
    def __init__(self,name):
        name=f"vaults/{name}"
        self.conn = sqlite3.connect(name,check_same_thread=False)
        self.c = self.conn.cursor()
        
    def newwrite(self, name, uname, pas, url):
        conn = self.conn
        c=self.c
        try:

            c.execute(
                """CREATE TABLE IF NOT EXISTS  passwords
                (date timestamp,name text, username text, password text, url text DEFAULT 'o' )"""
            )
        except Exception as e:
            print(e)

        time = datetime.now()
        c.execute(
            "INSERT INTO passwords VALUES (?,?,?,?,?)", (time, name, uname, pas, url)
        )
        conn.commit()
        conn.close()
    
    
    def update(self, name, uname, pas, url, name2, uname2):
        c = self.c
        conn = self.conn
        date = datetime.now()
        c.execute("""UPDATE passwords SET date = ?, name = ?, username= ?, password = ?, url = ? WHERE name = ? and username = ? and date < ? """, (date, name, uname, pas, url, name2, uname2,date))
        result=c.rowcount
        conn.commit()
        conn.close()
        return result

    def delete(self,name,uname):
        c=self.c
        conn=self.conn
        c.execute("""delete from passwords where name LIKE ? and username LIKE ? COLLATE NOCASE """,(name,uname))
        result = c.rowcount
        conn.commit()
        conn.close()
        return result
 

class writenote:
    def __init__(self,name):
        name=f"vaults/{name}"
        self.conn = sqlite3.connect(name,check_same_thread=False)
        self.c = self.conn.cursor()
        
    def newwrite(self,title,note):
        conn = self.conn
        c=self.c
        try:

            c.execute(
                """CREATE TABLE IF NOT EXISTS  notes
                (date timestamp,title text, note text )"""
            )
        except Exception as e:
            print(e)

        time = datetime.now()
        c.execute(
            "INSERT INTO notes VALUES (?,?,?)", (time, title,note)
        )
        conn.commit()
        conn.close()

class writecards:
    def __init__(self,name):
        name=f"vaults/{name}"
        self.conn = sqlite3.connect(name,check_same_thread=False)
        self.c = self.conn.cursor()
        
    def newwrite(self,name,type,number,code,sdate,edate):
        conn = self.conn
        c=self.c
        try:

            c.execute(
                """CREATE TABLE IF NOT EXISTS  cards
                (name text,type text, number text,security_code text,sdate text,edate text )"""
            )
        except Exception as e:
            print(e)

        c.execute(
            "INSERT INTO cards VALUES (?,?,?,?,?,?)", (name,type,number,code,sdate,edate)
        )
        conn.commit()
        conn.close()

    
    

