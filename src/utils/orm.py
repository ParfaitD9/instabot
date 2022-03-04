import sqlite3

DB_PATH = 'src/database.db3'

def set_message_default(message_id):
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.execute('UPDATE messages SET actual=0 WHERE actual=?', (1,))
        cur.execute('UPDATE messages SET actual=1 WHERE id=?', (message_id,))
    except Exception as e:
        print(f'{e.__class__} : {e}')
        con.rollback()
        r = {'status' : False, 'message' : e.args[0]}
    else:
        print(f'Message {message_id} set default')
        con.commit()
        r = {'status' : True, 'message' : f'Message {message_id} set default'}
    finally:
        cur.close()
        con.close()

        return r

def messages_existants():
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.execute('SELECT * FROM messages')
    except Exception as e:
        print(f'{e.__class__} : {e}')
        con.rollback()
        r = {'status' : False, 'message' : e.args[0]}
    else:
        r = {'status' : True, 'message' : f'SUCCES', 'data' : cur.fetchall()}
    finally:
        cur.close()
        con.close()

    return r

def insert_followers(followers):
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.executemany('INSERT INTO users (username) VALUES (?)', [(follower,) for follower in followers])
    except sqlite3.IntegrityError as e:
        print(e)
        r = {'status' : True, 'message' : 'User already exists'}
    except Exception as e:
        print(f'{e.__class__} : {e}')
        con.rollback()
        r = {'status' : False, 'message' : e.args[0]}
    else:
        print('Insertion done')
        con.commit()
        r = {'status' : True, 'message' : 'Insertion done'}
    finally:
        cur.close()
        con.close()

        return r

def update_user(user):
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.execute('UPDATE users SET pinned=1 WHERE username= ?', (user,))
    except Exception as e:
        print(f'{e.__class__} : {e}')
        con.rollback()
        r = {'status' : False, 'message' : e.args[0]}
    else:
        print(f'User {user} updated')
        con.commit()
        r = {'status' : True, 'message' : f'User {user} updated'}
    finally:
        cur.close()
        con.close()

        return r

def add_new_message(message, set_default= False):
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.execute('INSERT INTO messages (message) VALUES (?)', (message,))
    except sqlite3.IntegrityError as e:
        print(e)
        r = {'status' : True, 'message' : 'Message already exists'}
    except Exception as e:
        print(f'{e.__class__} : {e}')
        con.rollback()
        r = {'status' : False, 'message' : e.args[0]}
    else:
        print('New message added')
        con.commit()
        r = {'status' : True, 'message' : 'New message added'}
    finally:
        cur.close()
        con.close()

        return r

def all_users():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute('SELECT * FROM users')
    except Exception as e:
        print(e)
        r = {
            'status' : False,
            'data' : e.args[0]
        }
    else:
        r =  {
            'status' : True,
            'data' : cur.fetchall()
        }
    finally:
        cur.close()
        con.close()
    
    return r

def pinned_users():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute('SELECT * FROM users WHERE pinned=?', (1,))
    except Exception as e:
        print(e)
        r = {
            'status' : False,
            'data' : e.args[0]
        }
    else:
        r =  {
            'status' : True,
            'data' : cur.fetchall()
        }
    finally:
        cur.close()
        con.close()
    
    return r

def not_pinned_users():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute('SELECT * FROM users WHERE pinned=?', (0,))
    except Exception as e:
        print(e)
        r = {
            'status' : False,
            'data' : e.args[0]
        }
    else:
        r =  {
            'status' : True,
            'data' : cur.fetchall()
        }
    finally:
        cur.close()
        con.close()
    
    return r

def get_default_message() -> dict:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute('SELECT message FROM messages WHERE actual=?', (1,))
    except Exception as e:
        print(e)
        r = {
            'status' : False,
            'data' : e.args[0]
        }
    else:
        r =  {
            'status' : True,
            'data' : cur.fetchone()[0]
        }
    finally:
        cur.close()
        con.close()
    
    return r

if __name__ == '__main__':
    set_message_default(5)
    print(get_default_message())