from altair import Data
from pandas import DataFrame
import psycopg

def get_user(user_id: int):
    query = f'''
    SELECT public_name, username, role, joined_at
    FROM
        users
    WHERE
        id = %(user_id)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'user_id': str(user_id)})
            return DataFrame(cur.fetchall())

def verify_user(username: str):
    query = f'''
    SELECT users.id, users.role, auth.password
    FROM
        users JOIN authorizations AS auth ON users.id = auth.user_id
    WHERE
        username = %(username)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'username': username})
            return DataFrame(cur.fetchall())

def get_max_id():
    query = f'''
    SELECT MAX(id)
    FROM
        users
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return DataFrame(cur.fetchall())

def add_user(user_id, public_name, username, email, password):
    query_1 = f'''
    INSERT INTO users (id, public_name, username, email, role, joined_at)
    VALUES (%(id)s, %(public_name)s, %(username)s, %(email)s, 'user', CURRENT_TIMESTAMP(0))
    '''
    query_2 = f'''
    INSERT INTO authorizations (user_id, password)
    VALUES (%(user_id)s, %(password)s)
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query_1, {'id': str(user_id), 'public_name': public_name, 'username': username, 'email': email})
            cur.execute(query_2, {'user_id': str(user_id), 'password': password})

def check_follow(sub_id, user_id):
    query_1 = f'''
    SELECT * FROM follows
    WHERE
        following_user_id = %(sub_id)s AND
        followed_user_id = %(user_id)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query_1, {'sub_id': str(sub_id), 'user_id': str(user_id)})
            return DataFrame(cur.fetchall())

def follow(sub_id, user_id):
    query_1 = f'''
    INSERT INTO follows (following_user_id, followed_user_id, started_at)
    VALUES (%(sub_id)s, %(user_id)s, CURRENT_TIMESTAMP(0))
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query_1, {'sub_id': str(sub_id), 'user_id': str(user_id)})

def unfollow(sub_id, user_id):
    query_1 = f'''
    DELETE FROM follows
    WHERE
        following_user_id = %(sub_id)s AND
        followed_user_id = %(user_id)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query_1, {'sub_id': str(sub_id), 'user_id': str(user_id)})


if __name__ == '__main__':
    print(get_user(1))
