from psycopg import OperationalError
import streamlit as st
import pandas as pd
from streamlit.runtime.state import session_state
from repos.books import get_user_books, add_chapter, get_chapter_num
from repos.users import get_user, follow, check_follow, unfollow

def show_user_info(user):
    st.markdown(f'# {user.iloc[0,0]}')
    st.write(f'Никнейм: {user.iloc[0,1]}')
    st.write(f'Роль: {user.iloc[0,2]}')
    st.write(f'Дата регистарции: {user.iloc[0,3]}')

def show_user_books(books, user_id):
    if len(books) == 0:
        return

    st.markdown('## Книги Автора')
    for i in range(len(books)):
        st.markdown(f'''
        ### [{books.iloc[i,1]}](%s)
        {books.iloc[i,2]}

        *Дата создания: {books.iloc[i,3]}*
        ''' % f'book?book_id={books.iloc[i,0]}')
        if st.session_state.get('my_user_id') == user_id or st.session_state.get('role') == 'admin':
            if st.button('Редактировать', key=i):
                st.session_state['saved_book_id'] = books.iloc[i,0]
                st.session_state['redacting'] = True
                st.switch_page('pages/book.py')
            if st.button('Добавить главу', key=-i-1) or st.session_state.get('execute_button_clicked'):
                st.session_state['execute_button_clicked'] = True
                c_title = st.text_input(label='Название', key=i+100)
                if c_title:
                    max_ch = int(get_chapter_num(books.iloc[i,0]).iloc[0,0])
                    add_chapter(books.iloc[i,0], max_ch+1, c_title, 'Текст главы.')
                    st.write('Глава добавлена!')
        if i != len(books) - 1:
            st.divider()


def show_user_page(user_id):
    st.title('Страница пользователя')
    if st.session_state.get('my_user_id'):
        if st.button('Вернуться к своей странице'):
            st.session_state['user_id'] = None
            st.switch_page(f'pages/user.py')
    user = get_user(user_id)
    if user.empty:
        st.write('Выбранного пользователя не существует!')
    else:
        show_user_info(user)
        if st.session_state.get('my_user_id') and st.session_state.get('my_user_id') != user_id:
            result = check_follow(st.session_state['my_user_id'], user_id)
            if result.empty:
                if st.button('Подписаться'):
                    follow(st.session_state['my_user_id'], user_id)
                    st.switch_page('pages/user.py')
            else:
                if st.button('Отписаться'):
                    unfollow(st.session_state['my_user_id'], user_id)
                    st.switch_page('pages/user.py')
        user_books = get_user_books(user_id)
        show_user_books(user_books, user_id)

if st.query_params.get('user_id'):
    show_user_page(st.query_params['user_id'])
elif st.session_state.get('user_id'):
    show_user_page(st.session_state['user_id'])
elif st.session_state.get('my_user_id'):
    show_user_page(st.session_state['my_user_id'])
else:
    st.write('Пользователь не выбран!')
    st.write('Авторизуйтесь или измените запрос.')

