import sqlite3
import bcrypt
import streamlit as st
from sqlalchemy import create_engine, Table, MetaData
from settings import ORG_DATABASES

def user_exists(username):
    conn = sqlite3.connect('user_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password, organization):
    conn = sqlite3.connect('user_management.db')
    c = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    c.execute('INSERT INTO users (username, password, organization) VALUES (?, ?, ?)', 
              (username, hashed_password, organization))
    conn.commit()
    conn.close()

def verify_user(username, password):
    user = user_exists(username)
    if user and bcrypt.checkpw(password.encode(), user[2].encode()):
        return user[3]
    return None

def create_organization(name):
    conn = sqlite3.connect('user_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO organizations (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def get_organizations():
    conn = sqlite3.connect('user_management.db')
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

def check_if_admin():
    #conn = sqlite3.connect('user_management.db')
    #c = conn.cursor()
    #c.execute('SELECT * FROM admins WHERE user = ?', (user,))
    #user = c.fetchone()
    #conn.close()
    #return user
    pass