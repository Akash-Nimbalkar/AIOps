import streamlit as st
import sqlite3
import bcrypt

def update_username(old_username, new_username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, old_username))
        conn.commit()
        st.success("Username updated successfully!")
        st.session_state["username"] = new_username
    except sqlite3.IntegrityError:
        st.error("That username is already taken.")
    conn.close()

def update_password(username, new_password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_pw, username))
    conn.commit()
    conn.close()
    st.success("Password updated successfully!")

def render():
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to access this page.")
        st.stop()

    st.markdown("## 🧾 Account Settings")
    st.markdown(f"Welcome **{st.session_state['username']}**! You can update your profile details below:")

    # Tabs for update
    tab1, tab2 = st.tabs(["✏️ Edit Username", "🔒 Change Password"])

    with tab1:
        new_username = st.text_input("New Username")
        if st.button("Update Username"):
            if new_username:
                update_username(st.session_state["username"], new_username)
            else:
                st.warning("Username cannot be empty.")

    with tab2:
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        if st.button("Update Password"):
            if new_password and confirm_password:
                if new_password == confirm_password:
                    update_password(st.session_state["username"], new_password)
                else:
                    st.error("Passwords do not match.")
            else:
                st.warning("Please fill in both password fields.")

    # Logout
    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.success("Logged out successfully.")
        st.rerun()
