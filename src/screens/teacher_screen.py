import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher, get_teacher_by_id
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np

from datetime import datetime

import pandas as pd

from src.database.config import supabase


from src.components.dialog_voice_attendance import voice_attendance_dialog


# Query param helpers for Streamlit compatibility across versions
def _get_query_params():
    try:
        return st.experimental_get_query_params()
    except Exception:
        return {}


def _set_query_params(**kwargs):
    try:
        # Streamlit expects values as lists (e.g. {'k': ['v']})
        params = {k: (v if isinstance(v, list) else [v]) for k, v in kwargs.items()}
        st.experimental_set_query_params(**params)
    except Exception:
        pass


# Fallback file-based session persistence (local file) to survive refreshes
def _session_file_path():
    import os
    return os.path.join(os.getcwd(), '.teacher_session.json')


def _write_session_file(teacher_id, last_iso):
    import json, os
    try:
        with open(_session_file_path(), 'w', encoding='utf-8') as f:
            json.dump({'teacher_id': teacher_id, 'last': last_iso}, f)
    except Exception:
        pass


def _read_session_file():
    import json, os
    try:
        p = _session_file_path()
        if not os.path.exists(p):
            return None
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def _clear_session_file():
    import os
    try:
        p = _session_file_path()
        if os.path.exists(p):
            os.remove(p)
    except Exception:
        pass
def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    # Session persistence: keep teacher logged in for 30 minutes since last activity
    now = datetime.now()
    last_active_iso = st.session_state.get('teacher_last_active')
    is_active = False
    if 'teacher_data' in st.session_state and last_active_iso:
        try:
            last_active = datetime.fromisoformat(last_active_iso)
            elapsed = (now - last_active).total_seconds()
            if elapsed < 30 * 60:  # 30 minutes
                is_active = True
                # refresh last active timestamp on page load/activity
                st.session_state['teacher_last_active'] = now.isoformat()
        except Exception:
            # malformed timestamp, force re-login
            st.session_state.pop('teacher_last_active', None)

    # If not in session_state, try restoring from URL query params: ?teacher=<id>&last=<iso>
    if not is_active and 'teacher_data' not in st.session_state:
        # Try restore from query params first
        params = _get_query_params()
        teacher_param = params.get('teacher')
        last_param = params.get('last')
        restored = False
        if teacher_param and last_param:
            try:
                teacher_id = int(teacher_param[0])
                last_iso = last_param[0]
                last_dt = datetime.fromisoformat(last_iso)
                elapsed = (now - last_dt).total_seconds()
                if elapsed < 30 * 60:
                    teacher = get_teacher_by_id(teacher_id)
                    if teacher:
                        st.session_state['teacher_data'] = teacher
                        st.session_state['teacher_last_active'] = now.isoformat()
                        is_active = True
                        restored = True
            except Exception:
                pass

        # Fallback: try file-based session persistence
        if not restored:
            sess = _read_session_file()
            if sess:
                try:
                    teacher_id = int(sess.get('teacher_id'))
                    last_iso = sess.get('last')
                    last_dt = datetime.fromisoformat(last_iso)
                    elapsed = (now - last_dt).total_seconds()
                    if elapsed < 30 * 60:
                        teacher = get_teacher_by_id(teacher_id)
                        if teacher:
                            st.session_state['teacher_data'] = teacher
                            st.session_state['teacher_last_active'] = now.isoformat()
                            is_active = True
                except Exception:
                    pass

    if is_active:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()





def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            st.session_state.pop('teacher_data', None)
            st.session_state.pop('teacher_last_active', None)
            # clear URL query params
            try:
                _set_query_params()
            except Exception:
                pass
            # clear session file
            _clear_session_file()
            st.rerun()


    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()


    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    


    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()


    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _, liveness = predict_attendance(img_np, require_liveness=False, detector_upsample=2)

                    if detected:
                        for sid, ok in detected.items():
                            student_id = int(sid)
                            # only count if liveness passed
                            passed = bool(ok)
                            if passed:
                                all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log  = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'recorded_at': current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)











def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)


    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub.get('total_students', 0)),
                ("🕰️", "Classes", sub.get('total_classes', 0)),
            ]

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub.get('section'),
                stats=stats
            )
            
            # Render share button directly in the main rendering path
            if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_id']}", icon=":material/share:"):
                share_subject_dialog(sub['name'], sub['subject_code'])
            st.space()
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found. Take attendance using the 'Take Attendance' tab first.")
        return
    
    data = []

    for r in records:
        ts = r.get('recorded_at')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)



    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False
    
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role ='teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        # set last active timestamp to keep session alive for 30 minutes
        now_iso = datetime.now().isoformat()
        st.session_state['teacher_last_active'] = now_iso
        # persist via URL query params so refresh keeps session
        try:
            _set_query_params(teacher=str(teacher['teacher_id']), last=now_iso)
        except Exception:
            pass
        # Also write to local session file as a reliable fallback
        try:
            _write_session_file(teacher['teacher_id'], now_iso)
        except Exception:
            pass
        return True
    

    return False
def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using password', text_alignment='center')
    st.space()
    st.space()

    # Check database status with diagnostic
    from src.database.config import test_supabase_connection
    is_connected, status_msg = test_supabase_connection()
    if not is_connected:
        st.error(f'🔴 {status_msg}')
        st.info('Unable to login. Please verify:')
        st.markdown('• Your internet connection is working')
        st.markdown('• Supabase service is online')
        st.markdown('• Your Supabase URL and API key are correct')

    teacher_username = st.text_input("Enter username", placeholder='ananyaroy')

    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            st.session_state['login_attempted'] = True
            if login_teacher(teacher_username, teacher_pass):
                st.toast("welcome back!", icon="👋")
                st.rerun()
            else:
                st.error("Invalid username and password combo or database offline")

    with btnc2:
        if st.button('Register Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'register'

    footer_dashboard()



def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Sucessfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"
    

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()



    st.header('Register your teacher profile')

    st.space()
    st.space()

    
    teacher_username = st.text_input("Enter username", placeholder='ananyaroy')

    teacher_name = st.text_input("Enter name", placeholder='Ananya Roy')

    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

    teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register now', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)


    with btnc2:
        if st.button('Login Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'login'

    footer_dashboard()