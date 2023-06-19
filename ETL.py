import os
import glob
import psycopg2
import pandas as pd
from sql_query import *

def main():

    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=**** password=****")
    cur = conn.cursor()

    process_data(cur,conn,ilepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    
    conn.close()
if __name__="__main__":
    main()