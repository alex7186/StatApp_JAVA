from sqlite3 import connect, Error
from datetime import datetime


def create_connection(db_file):
    conn = None
    try:
        conn = connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)

def connect_to_db(db_file='./db/server_log.db'):
    
    sql_create_logs_table = """ CREATE TABLE IF NOT EXISTS logs 
        ( time text, status text, message text ); """

    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS users 
        (access_key text, 
        invite_code text, 
        vk_id text, 
        access_status text, 
        date_registered text, 
        date_last_login text, 
        primary key(access_key) ); """

    sql_create_user_users_actions = """ CREATE TABLE IF NOT EXISTS users_actions
        (access_key text, 
        last10_arrays text, 
        last10_history text, 
        primary key(access_key) ); """
    
    conn = create_connection(db_file)
    if conn is not None:
        create_table(conn, sql_create_logs_table)
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_user_users_actions)

    else:
        dt_str = str(datetime.now())[:-7]
        print(str(datetime.now())[:-7], 'E', "CANT CONNECT TO DATABASE")

    return conn

def add_db_log(db_connection, db_cursor, category, message=''):
    return None
    try:
        dt_str = str(datetime.now())[:-7]
        db_cursor.execute(f""" INSERT INTO logs
            VALUES
            (
                "{str(dt_str)}", 
                "{str(category)}", 
                "{str(message)}"
            );"""
        )
        db_connection.commit()
        print("\t  {} {} \t{}".format(dt_str, category, message[:40]))
    except Exception:
        dt_str = str(datetime.now())[:-7]
        print(dt_str, 'E', "CANT COMMIT IN logs")

def register_user(
    db_connection, 
    db_cursor, 
    access_key, 
    invite_code, 
    vk_id, 
    access_status, 
    date_registered, 
    date_last_login):

    try:
        db_cursor.execute(f""" INSERT OR REPLACE INTO users
                VALUES
                (
                    "{str(access_key)}",
                    "{str(invite_code)}", 
                    "{str(vk_id)}",
                    "{str(access_status)}",
                    "{str(date_registered)}",
                    "{str(date_last_login)}"
                );"""
            )
        db_connection.commit()
    except Exception:
        dt_str = str(datetime.now())[:-7]
        print(dt_str, 'E', "CANT COMMIT IN users")

    update_users_actions_table(db_connection, db_cursor, access_key)

def search_user_by_access_key(db_connection, db_cursor, access_key):
    search_str = f"select * from users where access_key = '{access_key}';"
    try:
        return db_cursor.execute(search_str).fetchall()
    except Exception:
        dt_str = str(datetime.now())[:-7]
        print(dt_str, 'E', "CANT OPEN IN users")
        return []

def search_user_by_vk_id(db_connection, db_cursor, vk_id):
    search_str = f"select count(*) from users where vk_id = '{vk_id}';"
    count = 0
    try:
        count = db_cursor.execute(search_str).fetchall()[0][0]
    except Exception:
        dt_str = str(datetime.now())[:-7]
        print(dt_str, 'E', "CANT OPEN IN users")
    return count

def update_users_actions_table(
    db_connection, 
    db_cursor, 
    access_key, 
    last10_arrays=[
        {'arr_num':0, 'arr':[]}, {'arr_num':1, 'arr':[]}, {'arr_num':2, 'arr':[]}, 
        {'arr_num':3, 'arr':[]}, {'arr_num':4, 'arr':[]}, {'arr_num':5, 'arr':[]}, 
        {'arr_num':6, 'arr':[]}, {'arr_num':7, 'arr':[]}, {'arr_num':8, 'arr':[]}, 
        {'arr_num':9, 'arr':[]}, 
    ], 

    last10_history=[
        {'arr_type':'None', 'with_id':[]}, {'arr_type':'None', 'with_id':[]},
        {'arr_type':'None', 'with_id':[]}, {'arr_type':'None', 'with_id':[]},
        {'arr_type':'None', 'with_id':[]},
    ]
    ):


    str_s = f"""insert OR REPLACE into users_actions values
            (
                "{str(access_key)}",
                "{encode_sum_array(last10_arrays)}",
                "{encode_sum_history(last10_history)}"
            );"""
    try:
        db_cursor.execute(str_s)
        db_connection.commit()
    except Exception:
        dt_str = str(datetime.now())[:-7]
        print(dt_str, 'E', "CANT COMMIT IN users_actions")

def update_date_last_login(db_connection, db_cursor, access_key):
    dt_str = str(datetime.now().date())
    t_str = f"update users set date_last_login = '{dt_str}' where access_key = '{access_key}'"
    
    try:
        db_cursor.execute(t_str)
        db_connection.commit()
    except Exception:
        dt_str = str(datetime.now())[:-7]
        print(dt_str, 'E', "CANT COMMIT IN users_actions")

def search_user_history(db_connection, db_cursor, access_key):
    t_str = f"select last10_history from users_actions where access_key = '{access_key}'"
    hist = db_cursor.execute(t_str).fetchall()[0][0]
    return decode_sum_hist(hist)

def search_user_array(db_connection, db_cursor, access_key):
    t_str = f"select last10_arrays from users_actions where access_key = '{access_key}'"
    arr = db_cursor.execute(t_str).fetchall()[0][0]
    return decode_sum_array(arr)

def encode_sum_array(last10_arrays):

    return ''.join(['!'+str(row['arr_num'])+'?'+str(row['arr'])[1:-2] for row in last10_arrays])+'!'

def encode_sum_history(last10_history):

    return ''.join(['!'+str(row['arr_type'])+'?'+str(row['with_id'])[1:-1] for row in last10_history])+'!'

def decode_sum_array(last10_arrays_str):
    ret = []
    for row in last10_arrays_str.split('!')[1:-1]:
        row_str = row.split('?')
        arr = row_str[1].split(', ')
        ret.append({'arr_num':row_str[0], 'arr':arr if arr[0] != '' else []})

    return ret

def decode_sum_hist(last5_history_str):
    ret = []
    for row in last5_history_str.split('!')[1:-1]:
        row_str = row.split('?')
        arr = row_str[1].split(', ')
        ret.append({'arr_type':row_str[0], 'with_id':arr if arr[0] != '' else []})
        
    return ret

