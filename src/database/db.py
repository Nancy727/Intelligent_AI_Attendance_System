from src.database.config import supabase
import bcrypt
from datetime import datetime


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

    unique_subjects = []
    seen_subject_ids = set()
    for sub in subjects:
        subject_id = sub.get('subject_id')
        if subject_id in seen_subject_ids:
            continue
        seen_subject_ids.add(subject_id)
        unique_subjects.append(sub)

    # Calculate totals separately
    for sub in unique_subjects:
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
        unique_sessions = len({
            datetime.fromisoformat(log['recorded_at']).replace(minute=0, second=0, microsecond=0).isoformat()
            for log in attendance
            if log.get('recorded_at')
        })
        sub['total_classes'] = unique_sessions

    return unique_subjects


def  enroll_student_to_subject(student_id, subject_id):
    existing = _safe_execute(
        supabase.table('subject_students')
        .select('subject_student_id')
        .eq('student_id', student_id)
        .eq('subject_id', subject_id),
        default=[]
    )
    if existing:
        return existing

    data = {'student_id': student_id, "subject_id": subject_id}
    return _safe_execute(supabase.table('subject_students').insert(data), default=[])


def  unenroll_student_to_subject(student_id, subject_id):
    return _safe_execute(
        supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id),
        default=[]
    )



def get_student_subjects(student_id):
    rows = _safe_execute(supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id), default=[])

    unique_rows = []
    seen_subject_ids = set()
    for row in rows:
        subject = row.get('subjects') or {}
        subject_id = subject.get('subject_id')
        if subject_id in seen_subject_ids:
            continue
        seen_subject_ids.add(subject_id)
        unique_rows.append(row)

    return unique_rows


def get_student_attendance(student_id):
    return _safe_execute(supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id), default=[])


def create_attendance(logs):
    if not logs:
        return []

    unique_logs = []
    seen_batch_keys = set()

    for log in logs:
        student_id = log.get('student_id')
        subject_id = log.get('subject_id')
        recorded_at = log.get('recorded_at')

        if not student_id or not subject_id or not recorded_at:
            continue

        try:
            ts = datetime.fromisoformat(recorded_at)
        except Exception:
            # If the timestamp is malformed, skip the row rather than inserting bad data.
            continue

        batch_key = (student_id, subject_id, ts.replace(minute=0, second=0, microsecond=0).isoformat())
        if batch_key in seen_batch_keys:
            continue
        seen_batch_keys.add(batch_key)

        hour_start = ts.replace(minute=0, second=0, microsecond=0)
        hour_end = hour_start.replace(minute=59, second=59, microsecond=999999)

        existing = _safe_execute(
            supabase.table('attendance_logs')
            .select('attendance_id')
            .eq('student_id', student_id)
            .eq('subject_id', subject_id)
            .gte('recorded_at', hour_start.isoformat())
            .lte('recorded_at', hour_end.isoformat()),
            default=[]
        )

        if existing:
            continue

        unique_logs.append(log)

    if not unique_logs:
        return []

    return _safe_execute(supabase.table('attendance_logs').insert(unique_logs), default=[])

def get_attendance_for_teacher(teacher_id):
    return _safe_execute(supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id), default=[])

