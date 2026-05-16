

import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
import cv2
import math

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() 


    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings= []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #128 embedding

        encodings.append(np.array(face_descriptor))
    return encodings


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


def eye_aspect_ratio(eye):
    # compute the euclidean distances
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C) if C != 0 else 0
    return ear


def get_head_pose(shape, img_size):
    # 3D model points.
    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (0.0, -330.0, -65.0),        # Chin
        (-225.0, 170.0, -135.0),     # Left eye left corner
        (225.0, 170.0, -135.0),      # Right eye right corner
        (-150.0, -150.0, -125.0),    # Left Mouth corner
        (150.0, -150.0, -125.0)      # Right mouth corner
    ], dtype=np.float64)

    # 2D image points
    image_points = np.array([
        shape[30],     # Nose tip
        shape[8],      # Chin
        shape[36],     # Left eye left corner
        shape[45],     # Right eye right corner
        shape[48],     # Left Mouth corner
        shape[54]      # Right mouth corner
    ], dtype=np.float64)

    focal_length = img_size[1]
    center = (img_size[1] / 2, img_size[0] / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype=np.float64)

    dist_coeffs = np.zeros((4, 1))

    success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    # Convert to Euler angles
    rmat, _ = cv2.Rodrigues(rotation_vector)
    proj_matrix = np.hstack((rmat, translation_vector))
    eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6]
    # eulerAngles may be array-like; convert elements to floats (degrees)
    try:
        pitch = float(eulerAngles[0])
        yaw = float(eulerAngles[1])
        roll = float(eulerAngles[2])
    except Exception:
        # fallback to zeros
        pitch = 0.0
        yaw = 0.0
        roll = 0.0
    return {'pitch': pitch, 'yaw': yaw, 'roll': roll}


def laplacian_variance(gray):
    return cv2.Laplacian(gray, cv2.CV_64F).var()

@st.cache_resource
def get_trained_model():
    X = []
    y = []


    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) ==0:
        return 0
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {'clf': clf, 'X':X, "y":y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np, require_liveness=True, detector_upsample=1):
    detector, sp, facerec = load_dlib_models()
    faces = detector(class_image_np, detector_upsample)

    detected_student = {}
    liveness_info = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(faces), liveness_info
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for idx, face in enumerate(faces):
        shape = sp(class_image_np, face)
        shape_np = shape_to_np(shape)

        # compute face embedding
        face_descriptor = facerec.compute_face_descriptor(class_image_np, shape, 1)
        encoding = np.array(face_descriptor)

        # match to student
        predicted_id = None
        if len(all_students) >= 2:
            try:
                predicted_id = int(clf.predict([encoding])[0])
            except Exception:
                predicted_id = None
        elif len(all_students) == 1:
            predicted_id = int(all_students[0])

        if predicted_id is None:
            continue

        # compute texture analysis
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        h, w = class_image_np.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)
        face_roi = class_image_np[y1:y2, x1:x2]
        gray = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY)
        lap_var = laplacian_variance(gray)

        # head pose
        hp = get_head_pose(shape_np, class_image_np.shape)

        # eye aspect ratio
        leftEye = shape_np[36:42]
        rightEye = shape_np[42:48]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # liveness heuristics
        texture_ok = lap_var > 50.0
        pose_ok = abs(hp['yaw']) < 30 and abs(hp['pitch']) < 30
        blink_detected = ear < 0.20

        liveness_pass = texture_ok and pose_ok

        liveness_info[predicted_id] = {
            'laplacian_variance': float(lap_var),
            'head_pose': hp,
            'ear': float(ear),
            'blink': bool(blink_detected),
            'liveness_pass': bool(liveness_pass)
        }

        # final match threshold
        student_embedding = X_train[y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encoding)
        resemblance_threshold = 0.6
        if best_match_score <= resemblance_threshold:
            # Attendance photos can be group shots, so optionally skip the liveness gate.
            if (not require_liveness) or liveness_pass:
                detected_student[predicted_id] = True
            else:
                # still include but mark as suspicious
                detected_student[predicted_id] = False
    return detected_student, all_students, len(faces), liveness_info

