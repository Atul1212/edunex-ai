import streamlit as st
import requests
import pandas as pd

# --- CONFIG ---
API_GATEWAY = 'http://127.0.0.1:8000'

st.set_page_config(page_title='EduNex Portal', page_icon='', layout='wide')

if 'token' not in st.session_state:
    st.session_state['token'] = None

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

def dashboard():
    st.sidebar.title(' EduNex Menu')
    st.sidebar.success('Online')
    if st.sidebar.button('Logout'):
        st.session_state['token'] = None
        st.rerun()

    st.title(' EduNex ERP Dashboard')
    
    # --- TABS ---
    tab1, tab2, tab3, tab4 = st.tabs([' Courses', ' Admissions', ' Attendance', ' Finance'])

    # --- TAB 1: COURSES ---
    with tab1:
        st.header('Course List')
        if st.button('Refresh Courses'):
            st.rerun()
        try:
            res = requests.get(f'{API_GATEWAY}/academic/courses')
            if res.status_code == 200:
                courses = res.json()
                if courses:
                    st.dataframe(pd.DataFrame(courses)[['name', 'description', 'id']], use_container_width=True)
                else:
                    st.info('No courses found.')
        except: st.error('Failed to load courses')

    # --- TAB 2: ADMISSIONS ---
    with tab2:
        st.header('New Admission')
        with st.form('enroll_form'):
            u_id = st.text_input('User ID (UUID)')
            roll = st.text_input('Roll Number')
            addr = st.text_input('Address')
            c_id = st.text_input('Course ID (UUID)')
            if st.form_submit_button('Enroll'):
                payload = {'user_id': u_id, 'roll_number': roll, 'address': addr, 'course_id': c_id}
                res = requests.post(f'{API_GATEWAY}/academic/students', json=payload)
                if res.status_code == 200: st.success('Enrolled Successfully!')
                else: st.error(res.text)

    # --- TAB 3: ATTENDANCE ---
    with tab3:
        st.header('Daily Attendance')
        with st.form('att_form'):
            s_id = st.text_input('Student ID for Attendance')
            co_id = st.text_input('Course ID for Attendance')
            status = st.selectbox('Status', ['PRESENT', 'ABSENT'])
            if st.form_submit_button('Mark'):
                res = requests.post(f'{API_GATEWAY}/academic/attendance', json={'student_id': s_id, 'course_id': co_id, 'status': status})
                if res.status_code == 200: st.success('Marked!')
                else: st.error(res.text)

    # --- TAB 4: FINANCE (NEW) ---
    with tab4:
        st.header('Finance Module')
        f_tab1, f_tab2 = st.tabs(['Create Fee Type', 'Collect Payment'])
        
        with f_tab1:
            with st.form('fee_cat_form'):
                fname = st.text_input('Fee Name (e.g. Exam Fee)')
                famt = st.number_input('Amount', min_value=0.0)
                fdesc = st.text_input('Description')
                if st.form_submit_button('Create Category'):
                    res = requests.post(f'{API_GATEWAY}/finance/fee-categories', json={'name': fname, 'amount': famt, 'description': fdesc})
                    if res.status_code == 200:
                        st.success(f'Created: {fname}')
                        st.rerun()
            
            # Show Categories
            res = requests.get(f'{API_GATEWAY}/finance/fee-categories')
            if res.status_code == 200 and res.json():
                st.caption('Existing Fee Categories:')
                st.dataframe(pd.DataFrame(res.json())[['name', 'amount', 'id']])

        with f_tab2:
            with st.form('pay_form'):
                p_sid = st.text_input('Student ID (UUID)')
                p_cid = st.text_input('Fee Category ID (UUID)')
                p_amt = st.number_input('Amount Paid', min_value=1.0)
                if st.form_submit_button('Record Payment'):
                    res = requests.post(f'{API_GATEWAY}/finance/payments', json={'student_id': p_sid, 'category_id': p_cid, 'amount_paid': p_amt})
                    if res.status_code == 200: st.success('Payment Recorded!')
                    else: st.error(res.text)

if st.session_state['token'] is None: login()
else: dashboard()

