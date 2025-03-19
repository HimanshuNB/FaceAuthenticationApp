import tkinter as tk
from tkinter import messagebox
from face_auth_lib.face_auth import authenticate_user
from ui.password_manager import open_password_manager

class LoginWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Login")
        self.window.geometry("400x200")

        tk.Label(self.window, text="Face Authentication Login", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.window, text="Login with Face", command=self.login).pack(pady=10)

    def login(self):
        username, response = authenticate_user()
        if username:
            messagebox.showinfo("Login Successful", f"Welcome, {username}")
            self.window.destroy()
            open_password_manager(username)  # Open password manager after login
        else:
            messagebox.showerror("Login Failed", response)