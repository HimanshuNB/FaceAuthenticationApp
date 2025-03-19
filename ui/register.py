import tkinter as tk
from tkinter import messagebox
from face_auth_lib.face_auth import register_user

class RegisterWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Register")
        self.window.geometry("400x300")

        tk.Label(self.window, text="Name:").pack()
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack()

        tk.Label(self.window, text="Email:").pack()
        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack()

        tk.Label(self.window, text="Password:").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        tk.Button(self.window, text="Register", command=self.register).pack(pady=10)

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        response = register_user(name, email, password)
        messagebox.showinfo("Registration", response)
        if "successful" in response:
            self.window.destroy()