import streamlit as st
import requests
import pandas as pd
from datetime import date

# --- CONFIG ---
API_GATEWAY = 'http://127.0.0.1:8000'

st.set_page_config(page_title='EduNex Portal', page_icon='', layout='wide')

# --- SESSION STATE ---
if 'token' not in st.session_state:
    st.session_state['token'] = None

# --- LOGIN PAGE ---
def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title(' EduNex Login')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        if st.button('Login', use_container_width=True):
            try:
                response = requests.post(f'{API_GATEWAY}/auth/login', data={'username': email, 'password': password})
                if response.status_code == 200:
                    st.session_state['token'] = response.json().get('access_token')
                    st.rerun()
                else:
                    st.error('Invalid Credentials')
            except Exception as e:
                st.error(f'System Error: {e}')

# --- DASHBOARD PAGE ---
def dashboard():
    st.sidebar.title(' EduNex Menu')
    st.sidebar.info(f'Logged in as Admin')
    if st.sidebar.button('Logout'):
        st.session_state['token'] = None
        st.rerun()

    st.title(' Academic Dashboard')
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([' Courses', ' New Admission', ' Attendance'])

    # --- TAB 1: VIEW COURSES ---
    with tab1:
        st.header('Available Courses')
        if st.button('Refresh List'):
            st.rerun()
        try:
            res = requests.get(f'{API_GATEWAY}/academic/courses')
            if res.status_code == 200:
                courses = res.json()
                if courses:
                    df = pd.DataFrame(courses)
                    st.dataframe(df[['name', 'description', 'id']], use_container_width=True)
                else:
                    st.info('No courses found.')
        except Exception as e:
            st.error(f'Error: {e}')

    # --- TAB 2: ENROLL STUDENT ---
    with tab2:
        st.header('Student Enrollment Form')
        with st.form('enroll_form'):
            u_id = st.text_input('User ID (UUID)', placeholder='e.g., 999e4567...')
            roll = st.text_input('Roll Number', placeholder='e.g., ROLL-002')
            addr = st.text_input('Address')
            c_id = st.text_input('Course ID (UUID)', placeholder='Paste Course ID')
            if st.form_submit_button('Enroll Student'):
                payload = {'user_id': u_id, 'roll_number': roll, 'address': addr, 'course_id': c_id}
                res = requests.post(f'{API_GATEWAY}/academic/students', json=payload)
                if res.status_code == 200:
                    st.success(f'Student {roll} Enrolled!')
                else:
                    st.error(f'Error: {res.text}')

    # --- TAB 3: ATTENDANCE ---
    with tab3:
        st.header('Mark Attendance')
        with st.form('attendance_form'):
            s_id = st.text_input('Student ID (UUID)', placeholder='Paste Student ID here')
            co_id = st.text_input('Course ID (UUID)', placeholder='Paste Course ID here')
            status = st.selectbox('Status', ['PRESENT', 'ABSENT', 'LATE'])
            
            if st.form_submit_button('Mark Attendance'):
                payload = {'student_id': s_id, 'course_id': co_id, 'status': status}
                res = requests.post(f'{API_GATEWAY}/academic/attendance', json=payload)
                if res.status_code == 200:
                    st.success(f'Attendance Marked: {status}')
                else:
                    st.error(f'Error: {res.text}')
        
        st.divider()
        st.subheader('Check History')
        check_sid = st.text_input('Enter Student ID to View History')
        if st.button('View History'):
             res = requests.get(f'{API_GATEWAY}/academic/attendance/{check_sid}')
             if res.status_code == 200:
                 hist = res.json()
                 if hist:
                     st.dataframe(pd.DataFrame(hist)[['date', 'status']])
                 else:
                     st.info('No records found.')

# --- MAIN ROUTER ---
if st.session_state['token'] is None:
    login()
else:
    dashboard()

