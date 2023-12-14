import streamlit as st
import pandas as pd
import hashlib
import mysql.connector
from secret.credentials import *
from streamlit_extras.switch_page_button import switch_page


def init_connection():
    return mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )


conn = init_connection()
c = conn.cursor()


def create_usertable():
    c.execute(
        'CREATE TABLE IF NOT EXISTS Admin_Login(username VARCHAR(255),password VARCHAR(255))')
    conn.commit()


def add_userdata(username, password):
    c.execute('INSERT INTO Admin_Login(username,password) VALUES (%s,%s)',
              (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM Admin_Login WHERE username = %s AND password = %s',
              (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM Admin_Login')
    data = c.fetchall()
    return data


def close_connection():
    c.close()
    conn.close()


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def custom_css():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f1f5f8; /* Set the overall app background */
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
            .login-box {
                background-color: #ffffff; /* White color for the login box */
                border-radius: 10px;
                padding: 2em;
                margin: auto;
                width: 30%; /* Adjust the width of the login box */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
            }
            .stTextInput>div>div>input {
                border-radius: 20px; /* Rounded borders for input fields */
                border: 1px solid #ced4da;
                padding: 10px;
                margin-bottom: 1em;
                width: 100%;
                outline: none; /* Remove the outline */
            }
            .stTextInput>div>div>input:focus {
                outline: none; /* Specifically remove the outline on focus */
                border: 1px solid #ced4da; /* You can change the border color if needed */
            }
            .stButton>button {
                border-radius: 20px; /* Rounded borders for the button */
                border: none;
                padding: 10px 24px;
                display: block;
                width: 100%;
                margin-top: 20px;
                background-color: #0d6efd; /* Bootstrap primary button color */
                color: white;
            }

             /* Override the outline for focused input fields */
            .stTextInput input:focus, .stPassword input:focus, .stTextInput input:focus-visible, .stPassword input:focus-visible {
                outline: none !important;
                box-shadow: none !important;
                border: 1px solid #ced4da !important;
            }

            /* Remove the red border */
            .stTextInput input:focus-within {
                border-color: #ced4da !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    custom_css()
    st.subheader("ADMIN Login")
    with st.form(key='admin_login'):
        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')
        login_button = st.form_submit_button('LOGIN')

    if len(username) > 0 and len(password) > 0:
        if login_button:
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username, check_hashes(password, hashed_pswd))

            st.header(result)

            if result:
                st.success("LOGIN SUCCESSFUL")
                st.session_state['current_page'] = "ADMIN"
                switch_page("ADMIN")

            else:
                st.warning("Check the entered Username and password")

    close_connection()


if __name__ == '__main__':
    main()
