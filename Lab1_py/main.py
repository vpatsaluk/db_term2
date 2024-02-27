import psycopg2
from threading import Thread
import time
from tabulate import tabulate

db_params = {
    'host': 'localhost',
    'database': 'lab1_database',
    'user': 'postgres',
    'password': '1805',
    'port': '5432'
}

def db_default_values():
    conn = psycopg2.connect(database=db_params['database'], user=db_params['user'], password=db_params['password'],
                            host=db_params['host'], port=db_params['port'])
    cursor = conn.cursor()

    cursor.execute("UPDATE user_counter SET counter = 0, version = 0 WHERE user_id = 1")
    conn.commit()
    conn.close()

def db_select():
    conn = psycopg2.connect(database=db_params['database'], user=db_params['user'], password=db_params['password'],
                            host=db_params['host'], port=db_params['port'])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_counter")

    headers = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    conn.close()

    print(tabulate(data, headers, tablefmt='pretty'))

def lost_update():
    conn = psycopg2.connect(database=db_params['database'], user=db_params['user'], password=db_params['password'],
                            host=db_params['host'], port=db_params['port'])
    cursor = conn.cursor()

    for _ in range(10000):
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
        counter = cursor.fetchone()[0]
        counter += 1
        cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1", (counter,))
        conn.commit()

    conn.close()

def in_place_update():
    conn = psycopg2.connect(database=db_params['database'], user=db_params['user'], password=db_params['password'],
                           host=db_params['host'], port=db_params['port'])
    cursor = conn.cursor()

    for _ in range(10000):
        cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = 1")

        conn.commit()

    conn.close()

def row_level_locking():
    conn = psycopg2.connect(database=db_params['database'], user=db_params['user'], password=db_params['password'],
                            host=db_params['host'], port=db_params['port'])
    cursor = conn.cursor()

    for _ in range(10000):
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
        counter = cursor.fetchone()[0]
        counter += 1
        cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1", (counter,))
        conn.commit()

    conn.close()

def optimistic_concurrency_control():
    conn = psycopg2.connect(database=db_params['database'], user=db_params['user'], password=db_params['password'],
                            host=db_params['host'], port=db_params['port'])
    cursor = conn.cursor()

    for _ in range(10000):
        while True:
            cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
            counter, version = cursor.fetchone()
            counter += 1
            cursor.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = 1 AND version = %s",
                           (counter, version + 1, version))
            conn.commit()
            count = cursor.rowcount
            if count > 0:
                break

    conn.close()

if __name__ == '__main__':
    db_default_values()

    start_time = time.time()

    threads = []
    for _ in range(10):
        thread = Thread(target=lost_update)
        # thread = Thread(target=in_place_update)
        # thread = Thread(target=row_level_locking)
        # thread = Thread(target=optimistic_concurrency_control)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f'Execution time -> {time.time() - start_time:.3f} seconds')

    db_select()