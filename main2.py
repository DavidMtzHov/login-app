import streamlit as st
from views import *
import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import MyModel

# Create a form in Streamlit
name = st.text_input('Name')
description = st.text_area('Description')

if st.button('Add Entry'):
    # Save to the database
    entry = MyModel(name=name, description=description)
    entry.save()
    st.success('Entry added successfully!')

# Display entries from the database
entries = MyModel.objects.all()
for entry in entries:
    st.write(f"Name: {entry.name}, Description: {entry.description}")

from myapp2.models import MyModel2

# Create a form in Streamlit
name = st.text_input('Name2')
description = st.text_area('Description2')

if st.button('Add Entry2'):
    # Save to the database
    entry = MyModel2(name=name, description=description)
    entry.save()
    st.success('Entry added successfully!')

# Display entries from the database
entries = MyModel2.objects.all()
for entry in entries:
    st.write(f"Name: {entry.name}, Description: {entry.description}")


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
    elif st.query_params.view == 'admin':
        admin_view()