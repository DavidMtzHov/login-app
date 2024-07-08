import streamlit as st
from sqlalchemy import create_engine, Table, MetaData
import sqlite3

# Database configurations
ORG_DATABASES = {
    'organization_a': 'sqlite:///organization_a.db',
    'organization_b': 'sqlite:///organization_b.db',
}

# Dummy user data for login
USERS = {
    'user_a': {'password': 'password_a', 'organization': 'organization_a'},
    'user_b': {'password': 'password_b', 'organization': 'organization_b'},
}

# Function to create a connection to the database based on the organization
def get_db_connection(organization):
    if organization in ORG_DATABASES:
        #engine = create_engine(ORG_DATABASES[organization])
        engine = create_engine('sqlite:///user_management.db')
        return engine.connect()
    else:
        st.error("Organization database not found.")
        return None

# Function to verify user login
def verify_user(username, password):
    if username in USERS and USERS[username]['password'] == password:
        return USERS[username]['organization']
    return None

# Main app function
def main():
    st.title("Organization-specific Streamlit Application")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.organization = None
    
    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            organization = verify_user(username, password)
            if organization:
                st.session_state.logged_in = True
                st.session_state.organization = organization
                st.success(f"Logged in as {username}")
                st.rerun()
            else:
                st.error("Invalid username or password")
    else:
        organization = st.session_state.organization
        st.sidebar.write(f"Logged in as: {organization}")
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.organization = None
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
                st.write(result.fetchall())

if __name__ == "__main__":
    main()
