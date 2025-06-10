import streamlit as st

def render():
    # Title
    st.markdown("<h1 style='text-align: center;'>About</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Supervisor & Project Buddy
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Supervisor")
        st.markdown("""
        **Name:** Amit Badwaik  
        **Role:** Supervisor 
        """)

    with col2:
        st.subheader("Project Buddy")
        st.markdown("""
        **Name:** Shobha Korade  
        **Role:** Project Buddy  
        """)

    st.markdown("---")

    # Interns Section
    st.subheader("Interns")

    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown("### Intern 1")
        st.markdown("""
        **Name:** Akash Nimbalkar  
        **Role:** Intern
        """)

    with col4:
        st.markdown("### Intern 2")
        st.markdown("""
        **Name:** Chetan Phulmante  
        **Role:** Intern
        """)

    with col5:
        st.markdown("### Intern 3")
        st.markdown("""
        **Name:** Harsh Palande  
        **Role:** Intern
        """)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2025 Gen AI Team</p>", unsafe_allow_html=True)
