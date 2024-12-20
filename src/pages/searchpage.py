from psycopg import OperationalError
import streamlit as st
import pandas as pd
from repos.search import search_db

def search():
    options = ['Книги', 'Пользователи']
    selection = st.pills("Directions", options, selection_mode="single",
                         default='Книги')
    prompt_label = 'книг' if selection == 'Книги' else 'пользователей'
    prompt = st.text_input(f'Поиск {prompt_label}')
    if prompt:
        result = search_db(prompt, selection)
        if selection == 'Книги':
            books_result(result)
        elif selection == 'Пользователи':
            users_result(result)

def books_result(result):
    for i in range(len(result)):
        st.markdown(f'''
        ### {result.iloc[i,1]}
        ##### Автор: [{result.iloc[i,5]}](%s)
        {result.iloc[i,2]}

        *Дата создания: {result.iloc[i,3]}*
        ''' % f'user?user_id={result.iloc[i,4]}')
        if st.button('Открыть'):
            st.session_state['saved_book_id'] = result.iloc[i,0]
            st.switch_page(f'pages/book.py') #?book_id={book_id}&chapter_id={str(int(chapter_id)+1)}')
        if i != len(result) - 1:
            st.divider()
    
def users_result(result):
    for i in range(len(result)):
        st.markdown(f'''
        ### [{result.iloc[i,1]}](%s)
        ##### Автор: {result.iloc[i,2]}
        *Роль: {result.iloc[i,3]}*
        ''' % f'user?user_id={result.iloc[i,0]}')
        if i != len(result) - 1:
            st.divider()

search()
