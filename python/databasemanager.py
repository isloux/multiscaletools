#!/usr/bin/env python3

# See www.postgresqltutorial.com/postgresql-python/

from dotenv import load_dotenv
import os
import psycopg2

class psql_database:

    def __init__(self):
        load_dotenv()
        PSQLUSER = os.getenv("POSTGRESQLUSER")
        PSQLPASSWORD = os.getenv("POSTGRESQLPASSWORD")
        print(PSQLUSER, PSQLPASSWORD)
        try:
            self._conn = psycopg2.connect("dbname=timeseries user=" + PSQLUSER + " password=" + PSQLPASSWORD)
            cur = self._conn.cursor();
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
            print("Connection established")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnect(self):
        if self._conn is not None:
            self._conn.close()
            print("Connection closed")

    def add_table(self, tablename = "test1"):
        try:
            cur = self._conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS ''' + tablename + ''' ( \
                series_id int PRIMARY KEY, \
                filename CHAR(69), \
                nsteps INT);''')
            self._conn.commit()
            cur.close()
            print("Table {} created".format(tablename))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_table(self):
        try:
            cur = self._conn.cursor()
            cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public';")
            records = cur.fetchall()
            cur.close()
            return records
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def multiple_insert(self, insertlist, tablename = "test1"):
        try:
            sql = "INSERT INTO " + tablename + " VALUES %s;"
            cur = self._conn.cursor()
            cur.executemany(sql, insertlist)
            self._conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

if __name__ == "__main__":
    labase = psql_database()
    tablelist = labase.get_table()
    cleanlist = [ i[0] for i in tablelist ]
    if "test1" not in cleanlist:
        labase.add_table()
    labase.disconnect()
