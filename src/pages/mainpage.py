from psycopg import OperationalError
import streamlit as st
import pandas as pd
from repos.books import get_last_updated

def show_main_feed():
    st.title('Последние обновления')
    try:
        books = get_last_updated()
        for i in range(len(books)):
            st.markdown(f'''
            ### {books.iloc[i,1]}
            {books.iloc[i,2]}

            *Дата обновления: {books.iloc[i,3]}*
            ''')
            if st.button('Открыть', key=i):
                st.session_state['saved_book_id'] = books.iloc[i,0]
                st.switch_page(f'pages/book.py')
            if i != len(books) - 1:
                st.divider()
    except OperationalError:
        st.write('Ошибка подключения к БД!')

show_main_feed()
