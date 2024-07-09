import streamlit as st
from sqlalchemy import Table, MetaData
from functions import *
import time
import pandas as pd

def signup_view():
    username = st.text_input("Create username")
    password = st.text_input("Create password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    organizations = get_organizations()
    new_org = st.checkbox("Create a new organization")
    if new_org:
        organization = st.text_input("Organization Name")
    else:
        organization = st.selectbox("Select an organization", organizations)
    
    if st.button("Sign Up",type='primary'):
        if user_exists(username):
            st.error("Username already exists")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif new_org and not organization:
            st.error("Organization name cannot be empty")
        else:
            if new_org:
                create_organization(organization)
            create_user(username, password, organization)
            st.success("User created successfully! Please login.")
            st.query_params.view = "login"
            time.sleep(0.2)
            st.rerun()
    if st.button("Back to Login"):
        st.query_params.view = 'login'
        time.sleep(0.2)
        st.rerun()

def login_view():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c3:
        if st.button("Login",type='primary') or password:
            organization = verify_user(username, password)
            if organization:
                st.session_state.logged_in = True
                st.session_state.organization = organization
                st.success(f"Logged in as {username}")
                st.query_params.view = "main"
                time.sleep(0.2)
                st.rerun()
            else:
                st.error("Invalid username or password")
        if st.button("Sign Up"):
            st.query_params.view = "sign-up"
            time.sleep(0.2)
            st.rerun()

def main_view():
    organization = st.session_state.organization
    st.sidebar.write(f"Logged in as: {organization}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.organization = None
        st.query_params.view = 'login'
        time.sleep(0.2)
        st.rerun()
    
    if st.sidebar.button('Admin'):
        st.query_params.view = 'admin'
        time.sleep(0.2)
        st.rerun()
    
    conn = get_db_connection(organization)
    if conn:
        metadata = MetaData()
        metadata.reflect(bind=conn)
        
        # List all tables in the database
        table_names = metadata.tables.keys()
        selected_table = st.selectbox("Select a table to view", table_names)
        
        if selected_table:
            table = Table(selected_table, metadata, autoload_with=conn)
            query = table.select()
            result = conn.execute(query)
            
            st.write(f"Data from {selected_table}")
            rows = result.fetchall()
            df = pd.DataFrame(rows,columns=list(result.keys()))
            st.write(df)

            if 'email' not in st.session_state:
                st.session_state.email = None
            if 'name' not in st.session_state:
                st.session_state.name = None
            
            st.session_state.organization = organization
            user = st.text_input('Insert user name',key='name',value="",on_change=add_user)
            email = st.text_input('Insert user email:',key='email',value="",on_change=add_user)
            st.button('Submit',on_click=add_user)

def admin_view():
    st.title('This is the Admin View')