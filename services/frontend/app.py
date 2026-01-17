import streamlit as st
import requests
import pandas as pd
from datetime import date

# --- CONFIG ---
API_GATEWAY = 'http://127.0.0.1:8000'

st.set_page_config(page_title='EduNex Portal', page_icon='🎓', layout='wide')

if 'token' not in st.session_state:
    st.session_state['token'] = None

def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title('🔐 EduNex Login')
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
    st.sidebar.title('🎓 EduNex Menu')
    st.sidebar.success('Online')
    if st.sidebar.button('Logout'):
        st.session_state['token'] = None
        st.rerun()

    st.title('🏫 EduNex ERP Dashboard')
    
    # --- TABS ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['📋 Courses', '➕ Admissions', '📅 Attendance', '💰 Finance', '📝 Exams', '📧 Alerts'])

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

    # --- TAB 4: FINANCE ---
    with tab4:
        st.header('Finance Module')
        f_tab1, f_tab2 = st.tabs(['Create Fee Type', 'Collect Payment'])
        with f_tab1:
            with st.form('fee_cat_form'):
                fname = st.text_input('Fee Name')
                famt = st.number_input('Amount', min_value=0.0)
                fdesc = st.text_input('Description')
                if st.form_submit_button('Create Category'):
                    res = requests.post(f'{API_GATEWAY}/finance/fee-categories', json={'name': fname, 'amount': famt, 'description': fdesc})
                    if res.status_code == 200: st.success(f'Created: {fname}')
        with f_tab2:
            with st.form('pay_form'):
                p_sid = st.text_input('Student ID (UUID)')
                p_cid = st.text_input('Fee Category ID (UUID)')
                p_amt = st.number_input('Amount Paid', min_value=1.0)
                if st.form_submit_button('Record Payment'):
                    res = requests.post(f'{API_GATEWAY}/finance/payments', json={'student_id': p_sid, 'category_id': p_cid, 'amount_paid': p_amt})
                    if res.status_code == 200: st.success('Payment Recorded!')
                    else: st.error(res.text)

    # --- TAB 5: EXAMS ---
    with tab5:
        st.header('Examination Cell')
        e_tab1, e_tab2 = st.tabs(['Schedule Exam', 'Upload Marks'])
        with e_tab1:
            with st.form('exam_form'):
                ename = st.text_input('Exam Name')
                ecid = st.text_input('Course ID (UUID)')
                edate = st.date_input('Exam Date')
                etotal = st.number_input('Total Marks', value=100)
                if st.form_submit_button('Schedule Exam'):
                    payload = {'name': ename, 'course_id': ecid, 'date': str(edate), 'total_marks': etotal}
                    res = requests.post(f'{API_GATEWAY}/exam/exams', json=payload)
                    if res.status_code == 200:
                        st.success(f'Exam Scheduled: {ename}')
                        st.info(f'Exam ID: {res.json()["id"]}')
                    else: st.error(res.text)
        with e_tab2:
            with st.form('marks_form'):
                m_eid = st.text_input('Exam ID (UUID)')
                m_sid = st.text_input('Student ID (UUID)')
                marks = st.number_input('Marks Obtained', max_value=100.0)
                rem = st.text_input('Remarks')
                if st.form_submit_button('Submit Result'):
                    payload = {'exam_id': m_eid, 'student_id': m_sid, 'marks_obtained': marks, 'remarks': rem}
                    res = requests.post(f'{API_GATEWAY}/exam/results', json=payload)
                    if res.status_code == 200: st.success('Result Uploaded!')
                    else: st.error(res.text)

    # --- TAB 6: COMMUNICATION (NEW) ---
    with tab6:
        st.header('Communication Center')
        c_tab1, c_tab2 = st.tabs(['Send Email', 'Email Logs'])
        
        with c_tab1:
            st.caption('Simulate sending email alerts to students')
            with st.form('email_form'):
                recip = st.text_input('Recipient Email', placeholder='student@example.com')
                subj = st.text_input('Subject', placeholder='Result Declaration')
                cont = st.text_area('Message Content')
                if st.form_submit_button('Send Email'):
                    payload = {'recipient': recip, 'subject': subj, 'content': cont}
                    res = requests.post(f'{API_GATEWAY}/communication/send-email', json=payload)
                    if res.status_code == 200: st.success('Email Sent Successfully!')
                    else: st.error(res.text)

        with c_tab2:
            if st.button('Refresh Logs'):
                res = requests.get(f'{API_GATEWAY}/communication/logs')
                if res.status_code == 200 and res.json():
                    st.dataframe(pd.DataFrame(res.json())[['recipient', 'subject', 'status', 'timestamp']], use_container_width=True)
                else:
                    st.info('No logs found.')

if st.session_state['token'] is None: login()
else: dashboard()