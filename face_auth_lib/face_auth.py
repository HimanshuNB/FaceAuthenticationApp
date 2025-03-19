import cv2
import face_recognition
import sqlite3
from encryption.encrypt import encrypt_face_data, decrypt_face_data, hash_password, verify_password

def capture_face():
    """Captures a real-time image from the webcam, detects a face, and returns its encoding."""
    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        cv2.imshow("Capturing Face - Press 's' to Save", frame)

        # Wait for 's' key to save the image
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Convert frame to RGB for face_recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)

    if not face_locations:
        print("No face detected. Try again.")
        return None

    # Encode the detected face
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    return face_encodings[0] if face_encodings else None

def register_user(name, email, password):
    """Registers a new user by capturing a face, encrypting the face data, and storing it in the database."""
    print("Please align your face in the camera and press 's' to capture.")
    face_data = capture_face()
    
    if face_data is None:
        return "No face detected!"

    encrypted_face = encrypt_face_data(face_data)
    password_hash = hash_password(password)

    conn = sqlite3.connect("database/face_auth.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email, face_data, password_hash) VALUES (?, ?, ?, ?)",
                       (name, email, encrypted_face, password_hash))
        conn.commit()
        return "Registration successful!"
    except sqlite3.IntegrityError:
        return "Email already registered!"
    finally:
        conn.close()

def authenticate_user():
    """Authenticates a user by capturing a face and comparing it with stored face encodings."""
    print("Align your face in the camera and press 's' to verify.")
    face_data = capture_face()
    
    if face_data is None:
        return None, "No face detected!"

    conn = sqlite3.connect("database/face_auth.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, face_data FROM users")
    users = cursor.fetchall()
    conn.close()

    for user in users:
        name, encrypted_face = user
        stored_embedding = decrypt_face_data(encrypted_face)

        match = face_recognition.compare_faces([stored_embedding], face_data)
        face_distance = face_recognition.face_distance([stored_embedding], face_data)

        if match[0] and face_distance[0] < 0.5:  # Face distance threshold
            return name, "Login Successful"
    
    return None, "Face not recognized."