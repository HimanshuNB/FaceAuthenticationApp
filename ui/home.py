import tkinter as tk
from tkinter import ttk
from ui.register import RegisterWindow
from ui.login import LoginWindow

class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Authentication App")
        self.root.geometry("400x300")

        tk.Label(root, text="Face Authentication", font=("Arial", 18, "bold")).pack(pady=20)

        ttk.Button(root, text="Register", command=self.open_register).pack(pady=10)
        ttk.Button(root, text="Login", command=self.open_login).pack(pady=10)

    def open_register(self):
        RegisterWindow(self.root)

    def open_login(self):
        LoginWindow(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    Home(root)
    root.mainloop()