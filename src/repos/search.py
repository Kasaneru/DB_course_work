from pandas import DataFrame
import psycopg

def search_db(prompt: str, domain: str | None):
    prompt = '%' + prompt + '%'
    if domain == 'Книги':
        return search_books(prompt)
    elif domain == 'Пользователи':
        return search_users(prompt)

def search_books(prompt: str):
    query = f'''
    SELECT books.id, books.title, books.description, books.created_at, users.id, users.public_name
    FROM
        books 
        JOIN writes ON writes.book_id = books.id
        JOIN users ON writes.author_id = users.id
    WHERE
        books.title ILIKE %(prompt)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'prompt': prompt})
            return DataFrame(cur.fetchall())

def search_users(prompt: str):
    query = f'''
    SELECT id, public_name, username, role
    FROM
        users
    WHERE
        public_name ILIKE %(prompt)s OR
        username ILIKE %(prompt)s
    '''
    with psycopg.connect('postgresql://postgres@localhost:5432/postgres') as conn:
        with conn.cursor() as cur:
            cur.execute(query, {'prompt': prompt})
            return DataFrame(cur.fetchall())

if __name__ == '__main__':
    print(search_db('Тихий', 'Книги'))
