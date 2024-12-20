from os.path import isfile
from psycopg import OperationalError
import streamlit as st
import pandas as pd
from repos.books import edit_chapter, get_book, get_chapter, get_chapters, get_chapter_num, get_comments, add_comment, get_max_com_id, get_book_tags, delete_comment
import os
from os.path import join

def show_book_page(book_id):
    st.title('Страница книги')
    book = get_book(book_id)
    if book.empty:
        st.warning('Выбранной книги не существует!')
    else:
        st.title(book.iloc[0, 1])
        st.markdown(f'{book.iloc[0, 2]}\n\n*Дата создания: {book.iloc[0,3]}*')
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f'Автор: {book.iloc[0, 5]}')
        with col2:
            if st.button('Перейти к автору'):
                st.session_state['user_id'] = book.iloc[0, 4]
                st.switch_page(f'pages/user.py')
        tags = get_book_tags(book.iloc[0,0])
        st.write('Теги: ', ', '.join(tags[0].tolist()))
        chapters = get_chapters(book_id)
        for i in range(len(chapters)):
            st.markdown(f'''
            ### {chapters.iloc[i,1]} {chapters.iloc[i,2]}

            *Дата создания: {chapters.iloc[i,3]}*
            ''')
            if st.button('Открыть', key=-i-1):
                st.session_state['saved_chapter'] = chapters.iloc[i, 1]
                st.switch_page(f'pages/book.py')
            if st.session_state.get('redacting') or st.session_state.get('role') == 'admin':
                if st.button('Редактировать', key=i) or st.session_state.get('execute_button_clicked'):
                    st.session_state['execute_button_clicked'] = True
                    chapter = get_chapter(book_id, i+1)
                    c_title = st.text_input(label='Название', value=chapter.iloc[0,1])
                    text = st.text_area(label='Содержание', value=chapter.iloc[0,3])
                    edit_chapter(book_id, i+1, c_title, text)
            if i != len(chapters) - 1:
                st.divider()


def show_page(book_id, chapter_id):
    book = get_book(book_id)
    if book.empty:
        st.warning('Выбранной книги не существует!')
        return

    st.title(book.iloc[0,1])
    chapter = get_chapter(book_id, chapter_id)
    chapter_num = get_chapter_num(book_id).iloc[0,0]
    # st.write(str(chapters))
    if int(chapter_id) > chapter_num:
        st.warning('Выбранной главы не существует!')
        return

    st.title(chapter.iloc[0, 1])
    st.markdown(chapter.iloc[0, 3])

    if int(chapter_id) < chapter_num:
        if st.button('Следующая глава'):
            st.session_state['saved_book_id'] = book_id
            st.session_state['saved_chapter'] = str(int(chapter_id)+1)
            st.switch_page(f'pages/book.py') #?book_id={book_id}&chapter_id={str(int(chapter_id)+1)}')

    if int(chapter_id) > 1:
        if st.button('Предыдущая глава'):
            st.session_state['saved_book_id'] = book_id
            st.session_state['saved_chapter'] = str(int(chapter_id)-1)
            st.switch_page(f'pages/book.py') 

    if st.button('Вернуться к книге'):
        st.session_state['saved_chapter'] = None
        st.switch_page(f'pages/book.py')

    show_comments(book_id, chapter_id)

def show_comments(book_id, chapter_id):
    st.markdown('### Комментарии')
    comments = get_comments(book_id, chapter_id)
    for i in range(len(comments)):
        st.markdown(f'''**{comments.iloc[i, 2]}** ({comments.iloc[i, 3]}) at *{comments.iloc[i, 6]}*
        
        {comments.iloc[i, 5]}
        ''')
        if st.session_state.get('role') == 'admin' or st.session_state.get('my_user_id') == comments.iloc[i,1]:
            if st.button('Удалить', key=i+200):
                delete_comment(comments.iloc[i,0])
                st.switch_page('pages/book.py')

        if i != len(comments) - 1:
            st.divider()

    if st.session_state.get('my_user_id'):
        if st.button('Оставить комментарий') or st.session_state.get('execute_button_clicked'):
            st.session_state['execute_button_clicked'] = True
            body = st.text_area('Комментарий')
            if body:
                max_id = int(get_max_com_id().iloc[0,0])
                add_comment(max_id+1, st.session_state['my_user_id'], chapter_id, body)

def main():
    #st.write(st.session_state)
    if st.session_state.get('saved_book_id') and st.session_state.get('saved_chapter'):
        show_page(st.session_state['saved_book_id'], st.session_state['saved_chapter'])
        return
    if st.session_state.get('saved_book_id'):
        show_book_page(st.session_state['saved_book_id'])
        return

    if st.query_params.get('book_id') and st.query_params.get('chapter'):
        show_page(st.query_params['book_id'], st.query_params['chapter'])
    elif st.query_params.get('book_id'):
        show_book_page(st.query_params['book_id'])
    else:
        st.write('Книга не выбрана!')

main()


