import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from encryption.encrypt import cipher  # Import encryption

class PasswordManager:
    def __init__(self, root, user_email):
        self.root = root
        self.user_email = user_email
        self.root.title("Password Manager")
        self.root.geometry("500x400")

        tk.Label(root, text="Password Manager", font=("Arial", 16, "bold")).pack(pady=10)

        # Form
        tk.Label(root, text="Website:").pack()
        self.website_entry = tk.Entry(root)
        self.website_entry.pack()

        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password:").pack()
        self.password_entry = tk.Entry(root)
        self.password_entry.pack()

        ttk.Button(root, text="Add Password", command=self.add_password).pack(pady=5)
        self.password_listbox = tk.Listbox(root)
        self.password_listbox.pack(fill=tk.BOTH, expand=True)
        ttk.Button(root, text="View Password", command=self.view_password).pack(pady=5)
        ttk.Button(root, text="Edit Password", command=self.edit_password).pack(pady=5)
        ttk.Button(root, text="Delete Password", command=self.delete_password).pack(pady=5)

        self.load_passwords()

    def encrypt_password(self, password):
        return cipher.encrypt(password.encode())

    def decrypt_password(self, encrypted_password):
        return cipher.decrypt(encrypted_password).decode()

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not website or not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        encrypted_password = self.encrypt_password(password)

        conn = sqlite3.connect("database/face_auth.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (user_email, website, username, password) VALUES (?, ?, ?, ?)",
                       (self.user_email, website, username, encrypted_password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password added successfully!")
        self.load_passwords()

    def load_passwords(self):
        self.password_listbox.delete(0, tk.END)
        conn = sqlite3.connect("database/face_auth.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, website FROM passwords WHERE user_email=?", (self.user_email,))
        for row in cursor.fetchall():
            self.password_listbox.insert(tk.END, f"{row[0]} - {row[1]}")
        conn.close()

    def view_password(self):
        selected = self.password_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No password selected!")
            return

        password_id = self.password_listbox.get(selected[0]).split(" - ")[0]

        conn = sqlite3.connect("database/face_auth.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM passwords WHERE id=?", (password_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            username, encrypted_password = result
            decrypted_password = self.decrypt_password(encrypted_password)
            messagebox.showinfo("Password Details", f"Username: {username}\nPassword: {decrypted_password}")

    def edit_password(self):
        selected = self.password_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No password selected!")
            return

        password_id = self.password_listbox.get(selected[0]).split(" - ")[0]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Password")
        edit_window.geometry("300x200")

        tk.Label(edit_window, text="New Password:").pack()
        new_password_entry = tk.Entry(edit_window)
        new_password_entry.pack()

        def save_new_password():
            new_password = new_password_entry.get()
            if not new_password:
                messagebox.showerror("Error", "Password cannot be empty!")
                return

            encrypted_new_password = self.encrypt_password(new_password)

            conn = sqlite3.connect("database/face_auth.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE passwords SET password=? WHERE id=?", (encrypted_new_password, password_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Password updated successfully!")
            edit_window.destroy()

        ttk.Button(edit_window, text="Save", command=save_new_password).pack(pady=10)

    def delete_password(self):
        selected = self.password_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No password selected!")
            return

        password_id = self.password_listbox.get(selected[0]).split(" - ")[0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this password?")
        if confirm:
            conn = sqlite3.connect("database/face_auth.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE id=?", (password_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Password deleted successfully!")
            self.load_passwords()

# Open Password Manager (Call this after user logs in)
def open_password_manager(user_email):
    password_manager_window = tk.Toplevel()
    PasswordManager(password_manager_window, user_email)