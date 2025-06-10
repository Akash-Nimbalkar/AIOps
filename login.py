import streamlit as st
import sqlite3
import bcrypt
import time
import importlib

st.set_page_config(
    page_title="Smart Log Assistant",
    layout="wide",
    page_icon="🔐"
)

# -----------------------
# Session Initialization
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = ""
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

# -----------------------
# Database Functions
# -----------------------
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode(), result[0].encode())
    return False

create_users_table()

# -----------------------
# UI Navigation
# -----------------------
def show_login_signup():
    st.title("🔐 Welcome to Smart Log Assistant")

    # Choose between login and sign up
    mode = st.radio("Select Mode", ["Login", "Sign Up"], index=0 if st.session_state.auth_mode == "Login" else 1)

    if mode == "Login":
        st.session_state.auth_mode = "Login"
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.success(f"Welcome {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "home"
                time.sleep(1.5)
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
                st.button("Forgot Password (Coming Soon)", disabled=True)

    elif mode == "Sign Up":
        st.session_state.auth_mode = "Sign Up"
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")

        if st.button("Sign Up"):
            if not new_user or not new_pass or not confirm_pass:
                st.warning("Please fill all fields.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            elif add_user(new_user, new_pass):
                st.success("Account created! Redirecting to login...")
                time.sleep(1.5)
                st.session_state.auth_mode = "Login"
                st.experimental_rerun()
            else:
                st.warning("Username already exists.")

# -----------------------
# Page Routing
# -----------------------
PAGES = {
    "home": "app_pages.home",
    "contact": "app_pages.contact",
    "about": "app_pages.about",
    "account": "app_pages.account"
}

def show_logged_in_ui():
    st.sidebar.title("📘 Navigation")
    choice = st.sidebar.radio("Go to", list(PAGES.keys()))
    module = importlib.import_module(PAGES[choice])
    module.render()

# -----------------------
# Main App Flow
# -----------------------
if not st.session_state.logged_in:
    show_login_signup()
else:
    show_logged_in_ui()

