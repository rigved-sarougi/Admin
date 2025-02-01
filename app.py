import streamlit as st
from auth import authenticate_user
from dashboard import admin_dashboard
from distributor_view import distributor_view

st.set_page_config(page_title="Sales Management System", layout="wide")

def main():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.sidebar.success(f"Logged in as {user.role.capitalize()}")
            if user.role == "admin":
                admin_dashboard()
            elif user.role == "distributor":
                distributor_view(user.id)
        else:
            st.sidebar.error("Invalid credentials")

if __name__ == "__main__":
    main()
