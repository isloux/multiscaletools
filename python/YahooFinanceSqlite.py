#!/usr/bin/env python

""" 
	Copyright 2016 Christophe Ramananjaona <isloux AT yahoo.co.uk>
"""

import sqlite3
import glob
from os.path import basename,splitext

class YahooFinancedata:

	def __init__(self,inputpath):
		self.files=glob.glob(inputpath+"*.data")

class sqlitedb:

	__timeformat=" 00:00:00.000"

	def __init__(self,dbname):
		self.conn=sqlite3.connect(dbname)
		print "Opened database successfully"

	def createTables(self):
		self.conn.execute('''CREATE TABLE RUSSELL3000NAMES
			(ID INT PRIMARY KEY     NOT NULL,
			NAME           TEXT     NOT NULL);''')
		self.conn.execute('''CREATE TABLE RUSSELL3000Q
			(NAMEID        INT     NOT NULL,
       			DATE           TEXT    NOT NULL,
       			OPEN           REAL    NOT NULL,
       			HIGH           REAL    NOT NULL,
       			LOW            REAL    NOT NULL,
       			CLOSE          REAL    NOT NULL,
       			VOLUME         INT);''')
		print "Table created successfully"

	def insertNames(self,inputpath):
		files=glob.glob(inputpath+"*.data")
		i=0
		for f in files:
        		i+=1
        		name=splitext(basename(f))[0]
        		self.conn.execute("INSERT INTO RUSSELL3000NAMES (ID,NAME) \
                		VALUES("+str(i)+",'"+name+"')")

		self.conn.commit()

	def __getId(self,name):
		try:
			cursor=self.conn.execute("SELECT ID FROM RUSSELL3000NAMES WHERE NAME='"+name+"'")
			return cursor.fetchone()[0]
		except:
			print "Symbol",name,"not found"
			raise

	def inputYahooQ(self,inputpath):
		for f in YahooFinancedata(inputpath).files:
			lq=[ line.split() for line in file(f) ]
			name=splitext(basename(f))[0]
			nameid=self.__getId(name)
			print "Inputting data for", name
			for q in lq: 
				dateandtime=q[0]+self.__timeformat
				openq=float(q[1])
				highq=float(q[2])
				lowq=float(q[3])
				closeq=float(q[4])
				volumeq=int(q[5])
				self.conn.execute("INSERT INTO RUSSELL3000Q (NAMEID,DATE,OPEN,HIGH,LOW,CLOSE,VOLUME) \
					VALUES("+str(nameid)+",'"+dateandtime+"',"+str(openq)+"," \
					+str(highq)+","+str(lowq)+","+str(closeq)+"," \
					+str(volumeq)+")")
		self.conn.commit()

	def getOneTickerDates(self,name,sdate,edate):
		sdate+=self.__timeformat
		edate+=self.__timeformat
		nameid=self.__getId(name)
		self.conn.row_factory=lambda cursor, row: row
		c=self.conn.cursor()
		ids=c.execute("SELECT DATE,OPEN,HIGH,LOW,CLOSE,VOLUME FROM RUSSELL3000Q WHERE NAMEID='"+ \
			str(nameid)+"' AND DATE BETWEEN '"+sdate+"' AND '"+edate+"'").fetchall()
		return ids

	def getTables(self):
		cursor=self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
		return cursor.fetchall()

	def getNames(self):
		cursor=self.conn.execute("SELECT NAME FROM RUSSELL3000NAMES;")
                return cursor.fetchall()

	def close(self):
		self.conn.close()

def main(dbname="test.db",inputpath="Russell3000/database/"):
	YahooQdb=sqlitedb(dbname)
	if len(YahooQdb.getTables())==0:
		YahooQdb.createTables()
		YahooQdb.insertNames(inputpath)
		YahooQdb.inputYahooQ(inputpath)
	YahooQdb.close()

if __name__ == "__main__":
    main()
