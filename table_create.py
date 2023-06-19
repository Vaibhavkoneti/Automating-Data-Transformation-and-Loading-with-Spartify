import psycopg2
from sql_query import create_table_queries,drop_table_queries


def create_databases():
    conn = psycopg2.connect("host=127.0.0.1 dbname=defaultdb user=**** password=**** ")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    conn.close()

    conn.psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=**** password=****")
    cur = conn.cursor()

    return cur,conn

def drop_tables(cur,conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tabbles(cur,conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
            


def main():
    cur,conn = create_databases()

    drop_tables(cur,conn)
    create_tables(cur,conn)

    conn.close()



if __name__ == "__main__":
    main()