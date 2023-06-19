import os
import glob
import psycopg2
import pandas as pd
from sql_query import *

def process_song_file(cur,filepath):
    df=pd.read_json(filepath,lines=True)
    for value in df.values:
        artist_id, artist_latitude, artist_location, artist_longitude, artist_name, duration, num_songs, song_id, title, year = value

        artist_data = [artist_id, artist_name, artist_location, artist_longitude, artist_latitude]
        cur.execute(artist_table_insert, artist_data)

        
        song_data = [song_id, title, artist_id, year, duration]
        cur.execute(song_table_insert, song_data)

def process_log_file(cur, filepath):
    df = pd.read_json(filepath, lines=True)
    df = df[df['page']=='NextSong']

    t = pd.to_datetime(df['ts'], unit='ms')

            # insert time data records
    time_data = []

    for line in t:
        time_data.append([line, line.hour, line.day, line.week, line.month, line.year, line.day_name()])
        column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
        time_df = pd.DataFrame.from_records(time_data, columns=column_labels)

    for i,row in time_df.iterrows():
        cur.execute(time_table_insert,list(row))

        user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

           
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
            
    for index, row in df.iterrows():
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
            
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
            
        songplay_data = (index, pd.to_datetime(row.ts, unit='ms'), int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
    
    return all_files


def main():


    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=**** password=****")
    cur = conn.cursor()

    process_data(cur,conn,ilepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    
    conn.close()
if __name__="__main__":
    main()