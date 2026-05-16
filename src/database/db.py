from src.database.config import supabase
import bcrypt


def _safe_execute(query, default=None):
    try:
        response = query.execute()
        return response.data
    except Exception:
        return default



def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    response = _safe_execute(supabase.table("teachers").select("username").eq("username", username), default=[])
    return len(response) > 0 



def create_teacher(username, password, name):

    data = { "username" : username, "password": hash_pass(password), "name": name}
    return _safe_execute(supabase.table("teachers").insert(data), default=[])


def teacher_login(username, password):
    response = _safe_execute(supabase.table("teachers").select("*").eq("username", username), default=[])
    if response:
        teacher = response[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_teacher_by_id(teacher_id):
    res = _safe_execute(supabase.table('teachers').select('*').eq('teacher_id', int(teacher_id)), default=[])
    if res:
        return res[0]
    return None


def get_all_students():
    return _safe_execute(supabase.table('students').select("*"), default=[])

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    return _safe_execute(supabase.table('students').insert(data), default=[])


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    return _safe_execute(supabase.table("subjects").insert(data), default=[])

def get_teacher_subjects(teacher_id):
    # Fetch basic subjects first (without complex aggregations)
    subjects = _safe_execute(
        supabase.table('subjects').select("*").eq("teacher_id", teacher_id),
        default=[]
    )

    # Calculate totals separately
    for sub in subjects:
        subject_id = sub['subject_id']
        
        # Get student count
        students = _safe_execute(
            supabase.table('subject_students').select('*').eq('subject_id', subject_id),
            default=[]
        )
        sub['total_students'] = len(students)
        
        # Get unique attendance sessions
        attendance = _safe_execute(
            supabase.table('attendance_logs').select('recorded_at').eq('subject_id', subject_id),
            default=[]
        )
        unique_sessions = len(set(log['recorded_at'] for log in attendance if log.get('recorded_at')))
        sub['total_classes'] = unique_sessions

    return subjects


def  enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    return _safe_execute(supabase.table('subject_students').insert(data), default=[])


def  unenroll_student_to_subject(student_id, subject_id):
    return _safe_execute(
        supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id),
        default=[]
    )



def get_student_subjects(student_id):
    return _safe_execute(supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id), default=[])


def get_student_attendance(student_id):
    return _safe_execute(supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id), default=[])


def create_attendance(logs):
    return _safe_execute(supabase.table('attendance_logs').insert(logs), default=[])

def get_attendance_for_teacher(teacher_id):
    return _safe_execute(supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id), default=[])

