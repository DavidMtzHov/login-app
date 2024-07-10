import streamlit as st
from views import *

password_guess = st.text_input('What is the password?',type='password')

if password_guess != st.secrets['password']:
    st.stop()

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