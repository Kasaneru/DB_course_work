from psycopg import OperationalError
import streamlit as st
import pandas as pd
from repos.users import get_user, verify_user, get_max_id, add_user
#from repos.crypt import check_password
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()  # Генерация соли
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

def signin():
    username = st.text_input('Username')
    password = st.text_input('Password')
    user_auth = verify_user(username)
    #st.dataframe(user_auth)
    if not user_auth.empty:
        is_valid = check_password(password, bytes(user_auth.iloc[0,2], 'utf-8'))
        if is_valid:
            st.write('Вы вошли в аккаунт!')
            st.session_state['my_user_id'] = user_auth.iloc[0,0]
            st.session_state['role'] = user_auth.iloc[0,1]
            # st.write(st.session_state)
        else:
            st.warning('Неверный юзернейм/пароль')
    else:
        if username:
            st.warning('Неверный юзернейм/пароль')

def signup():
    username = st.text_input('Username')
    public_name = st.text_input('Public name')
    email = st.text_input('Email')
    password = st.text_input('Password')

    if username and public_name and email and password:
        max_id = int(get_max_id().iloc[0,0])
        add_user(max_id+1, public_name, username, email, str(hash_password(password), encoding='utf-8'))
        st.write('Пользователь добавлен!')

def main():
    selection = st.segmented_control(
            '', ['Вход', 'Регистрация'], selection_mode='single', default='Вход')
    if selection == 'Вход':
        signin()
    elif selection == 'Регистрация':
        signup()

main()
