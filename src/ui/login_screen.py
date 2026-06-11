import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from modules.auth import login, register
from modules.exceptions import InvalidCredentials
from ui.dashboard import Dashboard

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager - Login")
        self.geometry("1280x720")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(11, weight=1) 

        self.label = ctk.CTkLabel(self, text="Secure Vault\nLogin", font=("Roboto", 24))
        self.label.grid(row=1, column=0, padx=20, pady=10)

        self.username_label = ctk.CTkLabel(self, text="Username", width=250, anchor="w")
        self.username_label.grid(row=2, column=0, padx=20, pady=(5, 0))
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.username_entry.grid(row=3, column=0, padx=20, pady=(0, 5))

        self.password_label = ctk.CTkLabel(self, text="Master Password", width=250, anchor="w")
        self.password_label.grid(row=4, column=0, padx=20, pady=(5, 0))
        
        self.password_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.password_frame.grid(row=5, column=0, padx=20, pady=(0, 10))
        
        self.password_entry = ctk.CTkEntry(self.password_frame, placeholder_text="Master Password", show="*", width=215)
        self.password_entry.grid(row=0, column=0)
        
        self.show_password_btn = ctk.CTkButton(
            self.password_frame, text="👁", width=30, 
            fg_color="transparent", 
            text_color=("gray14", "gray84"), 
            hover_color=("gray70", "gray30"),
            command=self.toggle_password_visibility)
        self.show_password_btn.grid(row=0, column=1, padx=(5, 0))

        self.info_label = ctk.CTkLabel(self, text="This master password is used to encrypt your vault.\nBecause we don't store it, it cannot be changed or recovered if lost.", text_color="gray50", font=("Roboto", 12))

        self.error_label = ctk.CTkLabel(self, text="", text_color="#fd4141")
        self.error_label.grid(row=7, column=0, padx=20, pady=0)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.handle_login)
        self.login_button.grid(row=8, column=0, padx=20, pady=10)

        self.or_label = ctk.CTkLabel(self, text="- or -", text_color=("gray50", "gray70"))
        self.or_label.grid(row=9, column=0, pady=(0, 10))

        self.register_link = ctk.CTkButton(
            self, 
            text="Register", 
            fg_color="transparent", 
            hover=False, 
            text_color="#FF8C00",
            font=("Roboto", 14, "underline"),
            command=self.show_register_ui
            )
        self.register_link.grid(row=10, column=0, padx=20, pady=(0, 10))

        self.register_button = ctk.CTkButton(
            self, 
            text="Register", 
            fg_color="transparent", 
            border_width=2,
            text_color=("#FF8C00", "#E67E22"),
            border_color=("#FF8C00", "#E67E22"),
            hover_color="#dadada",
            command=self.handle_register
        )
        
    def toggle_password_visibility(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def handle_login(self):
        self.error_label.configure(text="")

        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="Please fill in all fields.")
            return

        try:
            user = login(username, password)
        except InvalidCredentials as e:
            self.error_label.configure(text=str(e))
            return
        except Exception as e:
            self.error_label.configure(text=f"An unexpected error occurred: {e}")
            return
            
        # redirect to dashboard
        self.destroy()
        dashboard_app = Dashboard(user)
        dashboard_app.mainloop()

    def show_register_ui(self):
        self.error_label.configure(text="")
        self.label.configure(text="Secure Vault\nRegister")
        self.username_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.login_button.grid_forget()
        self.or_label.grid_forget()
        self.register_link.grid_forget()
        self.info_label.grid(row=6, column=0, padx=20, pady=(0, 10))
        self.register_button.grid(row=10, column=0, padx=20, pady=(0, 10))

    def show_login_ui(self):
        self.error_label.configure(text="")
        self.username_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.label.configure(text="Secure Vault\nLogin")
        self.info_label.grid_forget()
        self.register_button.grid_forget()
        self.login_button.grid(row=8, column=0, padx=20, pady=10)
        self.or_label.grid(row=9, column=0, pady=(0, 10))
        self.register_link.grid(row=10, column=0, padx=20, pady=(0, 10))


    def handle_register(self):
        self.error_label.configure(text="")

        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="Please fill in all fields.")
            return
        
        try:
            register(username, password)
            messagebox.showinfo("Success", "Registration successful! Please login with your new credentials.")
            self.register_button.grid_forget()
            self.show_login_ui()
        except Exception as e:
            self.error_label.configure(text=e)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    theme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'theme.json'))
    ctk.set_default_color_theme(theme_path)
    app = LoginWindow()
    app.mainloop()
