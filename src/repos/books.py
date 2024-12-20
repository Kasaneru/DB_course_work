from re import S
from pandas import DataFrame
import psycopg
# from settings import DB_CONFIG

def get_last_updated():
    query = 'SELECT * FROM v_last_updated'
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return DataFrame(cur.fetchall())

def get_user_books(user_id: int):
    query = f'''
    SELECT
        books.id, books.title, books.description, books.created_at
    FROM
        books JOIN writes ON books.id = writes.book_id
    WHERE
        writes.author_id = %(user_id)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'user_id': str(user_id)})
            return DataFrame(cur.fetchall())

def get_book(book_id :int):
    query = f'''
    SELECT books.id, books.title, books.description, books.created_at, users.id, users.public_name
    FROM
        books 
        JOIN writes ON books.id = writes.book_id
        JOIN users ON users.id = writes.author_id
    WHERE
        books.id = %(book_id)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'book_id': str(book_id)})
            return DataFrame(cur.fetchall())

def get_chapter(book_id, chapter):
    query = f'''
    SELECT c.book_id, c.title, c.created_at, c.data
    FROM
        books JOIN chapters AS c ON books.id = c.book_id
    WHERE
        books.id = %(book_id)s AND
        c.chapter_number = %(chapter)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'book_id': str(book_id), 'chapter': str(chapter)})
            return DataFrame(cur.fetchall())

def get_chapters(book_id):
    query = f'''
    SELECT c.book_id, c.chapter_number, c.title, c.created_at
    FROM
        books JOIN chapters AS c ON books.id = c.book_id
    WHERE
        books.id = %(book_id)s
    ORDER BY
        c.chapter_number
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'book_id': str(book_id)})
            return DataFrame(cur.fetchall())

def get_chapter_num(book_id):
    query = f'''
    SELECT MAX(c.chapter_number)
    FROM
        books JOIN chapters AS c ON books.id = c.book_id
    WHERE
        books.id = %(book_id)s
    GROUP BY
        c.book_id
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'book_id': str(book_id)})
            return DataFrame(cur.fetchall())

def edit_chapter(book_id, chapter, title, data):
    query = f'''
    UPDATE
        chapters
    SET
        title = %(title)s,
        data = %(data)s
    WHERE
        book_id = %(book_id)s AND
        chapter_number = %(chapter)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'book_id': str(book_id), 'chapter': str(chapter), 'title': title, 'data': data})

def add_chapter(book_id, chapter, title, data):
    query = f'''
    INSERT INTO
        chapters (id, book_id, title, chapter_number, created_at, data)
    VALUES
        (%(ch_id)s, %(book_id)s, %(title)s, %(ch_num)s, CURRENT_TIMESTAMP(0), %(data)s)
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            max_ch_id = int(get_max_ch_id().iloc[0,0])
            cur.execute(query, {'ch_id': str(max_ch_id+1), 'book_id': str(book_id), 'ch_num': str(chapter), 'title': title, 'data': data})

def get_comments(book_id, chapter):
    query = f'''
    SELECT cm.id, cm.user_id, u.public_name, u.username, cm.chapter_id, cm.body, cm.created_at
    FROM
        books JOIN chapters AS ch ON books.id = ch.book_id
        JOIN comments AS cm ON cm.chapter_id = ch.id
        JOIN users AS u ON u.id = cm.user_id
    WHERE
        ch.book_id = %(book_id)s AND ch.chapter_number = %(chapter)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'book_id': str(book_id), 'chapter': str(chapter)})
            return DataFrame(cur.fetchall())

def get_max_com_id():
    query = f'''
    SELECT MAX(id)
    FROM
        comments
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return DataFrame(cur.fetchall())

def get_max_ch_id():
    query = f'''
    SELECT MAX(id)
    FROM
        chapters
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return DataFrame(cur.fetchall())

def add_comment(cm_id, user_id, ch_id, data):
    query = f'''
    INSERT INTO comments (id, user_id, chapter_id, body, created_at)
    VALUES (%(cm_id)s, %(user_id)s, %(ch_id)s, %(body)s, CURRENT_TIMESTAMP(0))
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'cm_id': str(cm_id), 'user_id': str(user_id), 'ch_id': str(ch_id), 'body': data})

def delete_comment(cm_id):
    query = f'''
    DELETE FROM comments
    WHERE id = %(cm_id)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'cm_id': str(cm_id)})

def get_book_tags(book_id):
    query = f'''
    SELECT tags.tag_name
    FROM
        tags JOIN has_tags ON tags.id = has_tags.tag_id
    WHERE
        has_tags.book_id = %(book_id)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'book_id': str(book_id)})
            return DataFrame(cur.fetchall())


if __name__ == '__main__':
    print(get_last_updated())
    print(get_user_books(2))
