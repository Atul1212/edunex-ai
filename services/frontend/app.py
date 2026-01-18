import streamlit as st
import requests
import pandas as pd
import os

# --- CONFIGURATION ---
# Docker environment variable se URL lega, nahi to localhost use karega
API_GATEWAY = os.getenv('API_GATEWAY_URL', 'http://127.0.0.1:8000')

st.set_page_config(page_title='EduNex AI Portal', page_icon='🏫', layout='wide')

# --- SESSION STATE (Login Token) ---
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'ai_draft' not in st.session_state:
    st.session_state['ai_draft'] = ""

# --- LOGIN FUNCTION ---
def login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h1>🔐 EduNex AI ERP</h1>
            <p>Next-Gen School Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')
            
            if st.button('Login', use_container_width=True, type="primary"):
                try:
                    response = requests.post(f'{API_GATEWAY}/auth/login', data={'username': email, 'password': password})
                    if response.status_code == 200:
                        st.session_state['token'] = response.json().get('access_token')
                        st.success("Login Successful!")
                        st.rerun()
                    else:
                        st.error('Invalid Credentials')
                except Exception as e:
                    st.error(f'Connection Error: {e}')
                    st.info("Ensure Docker containers are running.")

# --- DASHBOARD FUNCTION ---
def dashboard():
    # --- SIDEBAR ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
        st.title('EduNex Menu')
        st.success('🟢 System Online')
        st.markdown("---")
        if st.button('🚪 Logout', use_container_width=True):
            st.session_state['token'] = None
            st.rerun()

    # --- MAIN TABS ---
    st.title('🏫 EduNex ERP Dashboard')
    
    # 7 Tabs: Overview (New) + 6 Features
    tab_home, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        '📊 Overview', '📋 Courses', '➕ Admissions', '📅 Attendance', '💰 Finance', '📝 Exams', '🤖 AI Alerts'
    ])

    # --- TAB 0: HOME / VISUAL DASHBOARD (NEW & BEAUTIFUL) ---
    with tab_home:
        st.markdown("### 🚀 Real-time Insights")
        
        # Fetching Data for Metrics (Try/Except to prevent crashes)
        try:
            total_courses = len(requests.get(f'{API_GATEWAY}/academic/courses').json())
        except: total_courses = 0
        
        try:
            logs = requests.get(f'{API_GATEWAY}/communication/logs').json()
            total_emails = len(logs)
        except: total_emails = 0
        
        # Mock Data for Visualization (Kyunki abhi database khali ho sakta hai)
        # Jab real data aayega to ye automate ho jayega
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Courses", total_courses, "+2 New")
        col2.metric("Active Students", "120", "+5 this week")  # Placeholder logic
        col3.metric("Emails Sent", total_emails, "AI Powered")
        col4.metric("Revenue Collected", "$4,500", "+12%")

        st.markdown("---")
        
        # Charts Section
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📈 Attendance Trends")
            chart_data = pd.DataFrame({
                'Days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                'Present': [110, 115, 108, 118, 112],
                'Absent': [10, 5, 12, 2, 8]
            }).set_index('Days')
            st.bar_chart(chart_data, color=["#00CC96", "#EF553B"])
            
        with c2:
            st.subheader("💰 Fee Collection")
            fee_data = pd.DataFrame({
                'Category': ['Tuition', 'Transport', 'Exam', 'Library'],
                'Amount': [2500, 1200, 500, 300]
            }).set_index('Category')
            st.bar_chart(fee_data, horizontal=True)

    # --- TAB 1: COURSES ---
    with tab1:
        st.header('Course Management')
        c_view, c_create = st.tabs(['📜 View Courses', '🆕 Add New Course'])
        
        with c_view:
            if st.button('Refresh Course List'):
                st.rerun()
            try:
                res = requests.get(f'{API_GATEWAY}/academic/courses')
                if res.status_code == 200:
                    courses = res.json()
                    if courses:
                        df = pd.DataFrame(courses)
                        st.dataframe(df[['name', 'description', 'id']], use_container_width=True, hide_index=True)
                    else:
                        st.info('No courses found.')
            except: st.error('Failed to load courses')

        with c_create:
            st.subheader("Launch a New Course")
            with st.form("new_course_form"):
                name = st.text_input("Course Name", placeholder="e.g. Python Masterclass")
                desc = st.text_area("Description", placeholder="e.g. From Zero to Hero")
                if st.form_submit_button("Create Course"):
                    try:
                        res = requests.post(f'{API_GATEWAY}/academic/courses', json={"name": name, "description": desc})
                        if res.status_code == 200:
                            st.success(f"Course '{name}' Created Successfully!")
                            st.rerun()
                        else: st.error(f"Error: {res.text}")
                    except Exception as e: st.error(f"System Error: {e}")

    # --- TAB 2: ADMISSIONS ---
    with tab2:
        st.header('Student Admission')
        with st.form('enroll_form'):
            col_a, col_b = st.columns(2)
            with col_a:
                u_id = st.text_input('User ID (UUID)')
                roll = st.text_input('Roll Number')
            with col_b:
                addr = st.text_input('Address')
                c_id = st.text_input('Course ID (UUID)')
            
            if st.form_submit_button('Enroll Student', type="primary"):
                res = requests.post(f'{API_GATEWAY}/academic/students', 
                                    json={'user_id': u_id, 'roll_number': roll, 'address': addr, 'course_id': c_id})
                if res.status_code == 200: st.success('Enrolled Successfully!')
                else: st.error(res.text)

    # --- TAB 3: ATTENDANCE ---
    with tab3:
        st.header('Daily Attendance')
        with st.form('att_form'):
            c1, c2, c3 = st.columns(3)
            with c1: s_id = st.text_input('Student ID')
            with c2: co_id = st.text_input('Course ID')
            with c3: status = st.selectbox('Status', ['PRESENT', 'ABSENT'])
            
            if st.form_submit_button('Mark Attendance'):
                res = requests.post(f'{API_GATEWAY}/academic/attendance', 
                                    json={'student_id': s_id, 'course_id': co_id, 'status': status})
                if res.status_code == 200: st.success('Attendance Marked!')
                else: st.error(res.text)

    # --- TAB 4: FINANCE ---
    with tab4:
        st.header('Finance Module')
        f_tab1, f_tab2 = st.tabs(['💳 Collect Payment', '📂 Create Fee Category'])
        
        with f_tab2:
            with st.form('fee_cat_form'):
                fname = st.text_input('Fee Name')
                famt = st.number_input('Amount', min_value=0.0)
                fdesc = st.text_input('Description')
                if st.form_submit_button('Create Category'):
                    res = requests.post(f'{API_GATEWAY}/finance/fee-categories', 
                                        json={'name': fname, 'amount': famt, 'description': fdesc})
                    if res.status_code == 200: st.success(f'Created: {fname}')

        with f_tab1:
            with st.form('pay_form'):
                p_sid = st.text_input('Student ID')
                p_cid = st.text_input('Fee Category ID')
                p_amt = st.number_input('Amount Paid', min_value=1.0)
                if st.form_submit_button('Record Payment'):
                    res = requests.post(f'{API_GATEWAY}/finance/payments', 
                                        json={'student_id': p_sid, 'category_id': p_cid, 'amount_paid': p_amt})
                    if res.status_code == 200: st.success('Payment Recorded!')
                    else: st.error(res.text)

    # --- TAB 5: EXAMS ---
    with tab5:
        st.header('Examination Cell')
        e_tab1, e_tab2 = st.tabs(['📅 Schedule Exam', '📝 Upload Results'])
        
        with e_tab1:
            with st.form('exam_form'):
                c1, c2 = st.columns(2)
                ename = c1.text_input('Exam Name')
                ecid = c2.text_input('Course ID')
                edate = c1.date_input('Exam Date')
                etotal = c2.number_input('Total Marks', value=100)
                if st.form_submit_button('Schedule Exam'):
                    res = requests.post(f'{API_GATEWAY}/exam/exams', 
                                        json={'name': ename, 'course_id': ecid, 'date': str(edate), 'total_marks': etotal})
                    if res.status_code == 200: 
                        st.success(f'Exam Scheduled! ID: {res.json().get("id")}')
                    else: st.error(res.text)

        with e_tab2:
            with st.form('marks_form'):
                m_eid = st.text_input('Exam ID')
                m_sid = st.text_input('Student ID')
                marks = st.number_input('Marks Obtained', max_value=100.0)
                rem = st.text_input('Remarks')
                if st.form_submit_button('Submit Result'):
                    res = requests.post(f'{API_GATEWAY}/exam/results', 
                                        json={'exam_id': m_eid, 'student_id': m_sid, 'marks_obtained': marks, 'remarks': rem})
                    if res.status_code == 200: st.success('Result Uploaded!')
                    else: st.error(res.text)

    # --- TAB 6: AI ALERTS (UPDATED WITH GEN-AI) ---
    with tab6:
        st.header('🤖 AI Communication Center')
        c_tab1, c_tab2 = st.tabs(['📧 Smart Email Sender', '📜 History Logs'])
        
        with c_tab1:
            st.info('💡 **GenAI Feature:** Type a topic, and AI will write the email for you.')
            
            # --- AI GENERATOR SECTION ---
            st.markdown("##### 1️⃣ Draft with AI")
            col_ai, col_btn = st.columns([3, 1])
            topic = col_ai.text_input("What is this email about?", placeholder="e.g. Warning for low attendance")
            
            if col_btn.button("✨ Generate Draft", use_container_width=True):
                if not topic:
                    st.warning("Please enter a topic first.")
                else:
                    with st.spinner("🤖 AI is thinking..."):
                        try:
                            # Call AI Engine via Gateway
                            ai_res = requests.post(f'{API_GATEWAY}/ai/generate', json={'prompt': topic, 'context': 'email'})
                            if ai_res.status_code == 200:
                                generated_text = ai_res.json().get('response')
                                st.session_state['ai_draft'] = generated_text
                                st.success("Draft Generated!")
                            else:
                                st.error(f"AI Error: {ai_res.text}")
                        except Exception as e:
                            st.error(f"Connection Error: {e}")

            st.divider()

            # --- SENDING SECTION ---
            st.markdown("##### 2️⃣ Review & Send")
            with st.form('email_form'):
                recip = st.text_input('Recipient Email', placeholder='student@example.com')
                subj = st.text_input('Subject', value=f"Notice: {topic}" if topic else "")
                
                # Auto-fill text area with AI content
                default_msg = st.session_state.get('ai_draft', '')
                cont = st.text_area('Message Content', value=default_msg, height=200)
                
                if st.form_submit_button('🚀 Send Email', type="primary"):
                    payload = {'recipient': recip, 'subject': subj, 'content': cont}
                    res = requests.post(f'{API_GATEWAY}/communication/send-email', json=payload)
                    if res.status_code == 200: st.success('Email Sent Successfully!')
                    else: st.error(res.text)

        with c_tab2:
            if st.button('Refresh Logs'):
                res = requests.get(f'{API_GATEWAY}/communication/logs')
                if res.status_code == 200:
                    data = res.json()
                    if data:
                        st.dataframe(pd.DataFrame(data)[['recipient', 'subject', 'status', 'timestamp']], use_container_width=True)
                    else: st.info("No logs found.")

# --- APP ENTRY POINT ---
if st.session_state['token'] is None:
    login()
else:
    dashboard()

# import streamlit as st
# import requests
# import pandas as pd
# from datetime import date


# import os  # <--- Make sure this is imported
# # ...
# # Docker se URL lega, warna Localhost use karega
# API_GATEWAY = os.getenv('API_GATEWAY_URL', 'http://127.0.0.1:8000')

# # --- CONFIG ---
# #API_GATEWAY = 'http://127.0.0.1:8000'

# st.set_page_config(page_title='EduNex Portal', page_icon='🎓', layout='wide')

# if 'token' not in st.session_state:
#     st.session_state['token'] = None

# def login():
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         st.title('🔐 EduNex Login')
#         email = st.text_input('Email')
#         password = st.text_input('Password', type='password')
#         if st.button('Login', use_container_width=True):
#             try:
#                 response = requests.post(f'{API_GATEWAY}/auth/login', data={'username': email, 'password': password})
#                 if response.status_code == 200:
#                     st.session_state['token'] = response.json().get('access_token')
#                     st.rerun()
#                 else:
#                     st.error('Invalid Credentials')
#             except Exception as e:
#                 st.error(f'System Error: {e}')

# def dashboard():
#     st.sidebar.title('🎓 EduNex Menu')
#     st.sidebar.success('Online')
#     if st.sidebar.button('Logout'):
#         st.session_state['token'] = None
#         st.rerun()

#     st.title('🏫 EduNex ERP Dashboard')
    
#     # --- TABS ---
#     tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['📋 Courses', '➕ Admissions', '📅 Attendance', '💰 Finance', '📝 Exams', '📧 Alerts'])

#     # --- TAB 1: COURSES ---
#     # --- TAB 1: COURSES (UPDATED) ---
#     with tab1:
#         st.header('Course Management')
        
#         # Humne Tab ko 2 hisso mein baata: List aur Create
#         c_view, c_create = st.tabs(['📜 View Courses', '🆕 Add New Course'])
        
#         # --- VIEW LIST ---
#         with c_view:
#             if st.button('Refresh List'):
#                 st.rerun()
#             try:
#                 res = requests.get(f'{API_GATEWAY}/academic/courses')
#                 if res.status_code == 200:
#                     courses = res.json()
#                     if courses:
#                         st.dataframe(pd.DataFrame(courses)[['name', 'description', 'id']], use_container_width=True)
#                     else:
#                         st.info('No courses found.')
#             except: st.error('Failed to load courses')

#         # --- CREATE COURSE FORM ---
#         with c_create:
#             st.subheader("Launch a New Course")
#             with st.form("new_course_form"):
#                 name = st.text_input("Course Name", placeholder="e.g. Python Masterclass")
#                 desc = st.text_area("Description", placeholder="e.g. Complete Python form Zero to Hero")
#                 submitted = st.form_submit_button("Create Course")
                
#                 if submitted:
#                     payload = {"name": name, "description": desc}
#                     try:
#                         res = requests.post(f'{API_GATEWAY}/academic/courses', json=payload)
#                         if res.status_code == 200:
#                             st.success(f"Course '{name}' Created Successfully!")
#                             st.rerun()
#                         else:
#                             st.error(f"Error: {res.text}")
#                     except Exception as e:
#                         st.error(f"System Error: {e}")

#     # --- TAB 2: ADMISSIONS ---
#     with tab2:
#         st.header('New Admission')
#         with st.form('enroll_form'):
#             u_id = st.text_input('User ID (UUID)')
#             roll = st.text_input('Roll Number')
#             addr = st.text_input('Address')
#             c_id = st.text_input('Course ID (UUID)')
#             if st.form_submit_button('Enroll'):
#                 payload = {'user_id': u_id, 'roll_number': roll, 'address': addr, 'course_id': c_id}
#                 res = requests.post(f'{API_GATEWAY}/academic/students', json=payload)
#                 if res.status_code == 200: st.success('Enrolled Successfully!')
#                 else: st.error(res.text)

#     # --- TAB 3: ATTENDANCE ---
#     with tab3:
#         st.header('Daily Attendance')
#         with st.form('att_form'):
#             s_id = st.text_input('Student ID for Attendance')
#             co_id = st.text_input('Course ID for Attendance')
#             status = st.selectbox('Status', ['PRESENT', 'ABSENT'])
#             if st.form_submit_button('Mark'):
#                 res = requests.post(f'{API_GATEWAY}/academic/attendance', json={'student_id': s_id, 'course_id': co_id, 'status': status})
#                 if res.status_code == 200: st.success('Marked!')
#                 else: st.error(res.text)

#     # --- TAB 4: FINANCE ---
#     with tab4:
#         st.header('Finance Module')
#         f_tab1, f_tab2 = st.tabs(['Create Fee Type', 'Collect Payment'])
#         with f_tab1:
#             with st.form('fee_cat_form'):
#                 fname = st.text_input('Fee Name')
#                 famt = st.number_input('Amount', min_value=0.0)
#                 fdesc = st.text_input('Description')
#                 if st.form_submit_button('Create Category'):
#                     res = requests.post(f'{API_GATEWAY}/finance/fee-categories', json={'name': fname, 'amount': famt, 'description': fdesc})
#                     if res.status_code == 200: st.success(f'Created: {fname}')
#         with f_tab2:
#             with st.form('pay_form'):
#                 p_sid = st.text_input('Student ID (UUID)')
#                 p_cid = st.text_input('Fee Category ID (UUID)')
#                 p_amt = st.number_input('Amount Paid', min_value=1.0)
#                 if st.form_submit_button('Record Payment'):
#                     res = requests.post(f'{API_GATEWAY}/finance/payments', json={'student_id': p_sid, 'category_id': p_cid, 'amount_paid': p_amt})
#                     if res.status_code == 200: st.success('Payment Recorded!')
#                     else: st.error(res.text)

#     # --- TAB 5: EXAMS ---
#     with tab5:
#         st.header('Examination Cell')
#         e_tab1, e_tab2 = st.tabs(['Schedule Exam', 'Upload Marks'])
#         with e_tab1:
#             with st.form('exam_form'):
#                 ename = st.text_input('Exam Name')
#                 ecid = st.text_input('Course ID (UUID)')
#                 edate = st.date_input('Exam Date')
#                 etotal = st.number_input('Total Marks', value=100)
#                 if st.form_submit_button('Schedule Exam'):
#                     payload = {'name': ename, 'course_id': ecid, 'date': str(edate), 'total_marks': etotal}
#                     res = requests.post(f'{API_GATEWAY}/exam/exams', json=payload)
#                     if res.status_code == 200:
#                         st.success(f'Exam Scheduled: {ename}')
#                         st.info(f'Exam ID: {res.json()["id"]}')
#                     else: st.error(res.text)
#         with e_tab2:
#             with st.form('marks_form'):
#                 m_eid = st.text_input('Exam ID (UUID)')
#                 m_sid = st.text_input('Student ID (UUID)')
#                 marks = st.number_input('Marks Obtained', max_value=100.0)
#                 rem = st.text_input('Remarks')
#                 if st.form_submit_button('Submit Result'):
#                     payload = {'exam_id': m_eid, 'student_id': m_sid, 'marks_obtained': marks, 'remarks': rem}
#                     res = requests.post(f'{API_GATEWAY}/exam/results', json=payload)
#                     if res.status_code == 200: st.success('Result Uploaded!')
#                     else: st.error(res.text)

#     # --- TAB 6: COMMUNICATION (NEW) ---
#     with tab6:
#         st.header('Communication Center')
#         c_tab1, c_tab2 = st.tabs(['Send Email', 'Email Logs'])
        
#         with c_tab1:
#             st.caption('Simulate sending email alerts to students')
#             with st.form('email_form'):
#                 recip = st.text_input('Recipient Email', placeholder='student@example.com')
#                 subj = st.text_input('Subject', placeholder='Result Declaration')
#                 cont = st.text_area('Message Content')
#                 if st.form_submit_button('Send Email'):
#                     payload = {'recipient': recip, 'subject': subj, 'content': cont}
#                     res = requests.post(f'{API_GATEWAY}/communication/send-email', json=payload)
#                     if res.status_code == 200: st.success('Email Sent Successfully!')
#                     else: st.error(res.text)

#         with c_tab2:
#             if st.button('Refresh Logs'):
#                 res = requests.get(f'{API_GATEWAY}/communication/logs')
#                 if res.status_code == 200 and res.json():
#                     st.dataframe(pd.DataFrame(res.json())[['recipient', 'subject', 'status', 'timestamp']], use_container_width=True)
#                 else:
#                     st.info('No logs found.')

# if st.session_state['token'] is None: login()
# else: dashboard()