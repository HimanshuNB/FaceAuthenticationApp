import sqlite3

def delete_user(email):
    conn = sqlite3.connect("database/face_auth.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()

    if cursor.rowcount > 0:
        print(f"User with email {email} deleted successfully!")
    else:
        print("User not found!")

    conn.close()

# Replace with the actual email
delete_user("")
