import streamlit as st
from sqlalchemy import create_engine, Table, MetaData
import sqlite3
import bcrypt
import time
import pandas as pd

# Database configurations
ORG_DATABASES = {
    'organization_a': 'sqlite:///organization_a.db',
    'organization_b': 'sqlite:///organization_b.db',
}

# Setup user management database
def get_user_db_connection():
    return sqlite3.connect('user_management.db')

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def user_exists(username):
    conn = get_user_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password, organization):
    conn = get_user_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('INSERT INTO users (username, password, organization) VALUES (?, ?, ?)', 
              (username, hashed_password, organization))
    conn.commit()
    conn.close()

def verify_user(username, password):
    user = user_exists(username)
    if user and check_password(password, user[2]):
        return user[3]
    return None

def create_organization(name):
    conn = get_user_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO organizations (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def get_organizations():
    conn = get_user_db_connection()
    c = conn.cursor()
    c.execute('SELECT name FROM organizations')
    organizations = [row[0] for row in c.fetchall()]
    conn.close()
    return organizations

# Function to create a connection to the database based on the organization
def get_db_connection(organization):
    if organization in ORG_DATABASES:
        engine = create_engine(ORG_DATABASES[organization])
        return engine.connect()
    else:
        st.error("Organization database not found.")
        return None
    
# Function to add organization
def add_user():
    if st.session_state.email is not None and st.session_state.name is not None and '@' in st.session_state.email:
        conn2 = sqlite3.connect(f'{st.session_state.organization}.db')
        c = conn2.cursor()
        user = st.session_state.name
        email = st.session_state.email
        c.execute("INSERT INTO users (name, email) VALUES (?, ?)",(user,email))
        conn2.commit()
        conn2.close()
        st.session_state.name = None
        st.session_state.email = None
        st.success('User added')
    else:
        st.error('Please make sure all fields are filled out and email has "@"')

#Views
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
    
    if st.button("Sign Up"):
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

# Main app function
def main():
    c1,c2,c3,c4,c5 = st.columns(5)
    with c3:
        st.write('# WFA')
    
    #Initialize logged in session
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.organization = None
    
    #Initialize views in session
    if 'view' not in st.query_params:
        st.query_params.view = 'login'

    if not st.session_state.logged_in:
        if st.query_params.view == "login":
            login_view()
        elif st.query_params.view == "sign-up":
            signup_view()
    else:    
        if st.query_params.view == "login":
            login_view()
        elif st.query_params.view == "main":
            main_view()
         

if __name__ == "__main__":
    main()
