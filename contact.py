import streamlit as st
from datetime import datetime
import json
import os
import time

DATA_FILE = "contact_messages.json"

def load_messages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # File is empty or corrupted
    return []


def save_message(name, email, message):
    messages = load_messages()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "message": message
    }
    messages.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(messages, f, indent=4)

def render():
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        return

    st.title("📬 Contact Us")

    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your Name", key="contact_name")
        email = st.text_input("Your Email", key="contact_email")
        message = st.text_area("Your Message", key="contact_message")
        submitted = st.form_submit_button("Send")

    if submitted and name and email and message:
        save_message(name, email, message)
        success_placeholder = st.empty()
        success_placeholder.success("Thanks for contacting us! We'll get back to you soon.")
        time.sleep(2)
        success_placeholder.empty()

    messages = load_messages()
    if messages:
        st.markdown("---")
        st.subheader("📩 Previous Messages")

        for idx, data in enumerate(reversed(messages)):
            with st.expander(f"📨 Message {len(messages)-idx}"):
                st.markdown(f"**📅 Date:** {data['timestamp']}")
                st.markdown(f"**👤 Name:** {data['name']}")
                st.markdown(f"**📧 Email:** {data['email']}")
                st.markdown("**📝 Message:**")
                st.write(data['message'])
