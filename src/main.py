import streamlit as st
from pages.mainpage import show_main_feed

def main():
    main_page = st.Page('pages/mainpage.py', title='Главная')
    search_page = st.Page('pages/searchpage.py', title='Поиск')
    book_page = st.Page('pages/book.py', title='Книги')
    profile_page = st.Page('pages/user.py', title='Профиль')
    login_page = st.Page('pages/login.py', title='Log in')
    pg = st.navigation([main_page, search_page, book_page, profile_page, login_page])
    pg.run()

if __name__ == '__main__':
    main()
