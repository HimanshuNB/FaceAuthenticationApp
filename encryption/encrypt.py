from cryptography.fernet import Fernet
import pickle
import bcrypt

# Generate encryption key (Keep this secret!)
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Encrypt & Decrypt Face Data
def encrypt_face_data(face_data):
    return cipher.encrypt(pickle.dumps(face_data))

def decrypt_face_data(encrypted_data):
    return pickle.loads(cipher.decrypt(encrypted_data))

# Hash & Verify Password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)