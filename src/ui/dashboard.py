import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from modules.vault import get_login_credentials
from modules.auth import login
from ui.credentials_popup import CredentialsPopup
from ui.new_login_popup import NewLoginPopup

testuser = login("testUser", "testpass")

class Dashboard(ctk.CTk):
    def __init__(self, user=testuser):
        super().__init__()

        self.user = user
        self.title(f"Secure Vault - {self.user.username}")
        self.geometry("1280x720")

        self.credentials_popup = None
        self.new_login_popup = None
        self._search_debounce_job = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Secure\nVault", font=ctk.CTkFont(size=20, weight="bold"), justify="left", anchor="w")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.logout_button = ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.handle_logout, text_color="gray10", fg_color="gray80", hover_color="gray60")
        self.logout_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Main
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20), padx=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        self.welcome_label = ctk.CTkLabel(header_frame, text=f"{self.user.username}'s Vault", font=ctk.CTkFont(size=24, weight="bold"))
        self.welcome_label.grid(row=0, column=0, sticky="w")

        self.new_credential_button = ctk.CTkButton(header_frame, text="+ New", font=ctk.CTkFont(size=16, weight="bold"), width=100, height=50, command=self.open_new_login_popup)
        self.new_credential_button.grid(row=0, column=1, sticky="e", padx=40)

        self.search_bar = ctk.CTkEntry(header_frame, placeholder_text="Search by domain...", width=250)
        self.search_bar.grid(row=1, column=0, columnspan=1, sticky="w", pady=(10, 0))
        self.search_bar.bind("<KeyRelease>", self.debounce_search)

        self.passwords_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        self.passwords_frame.grid(row=1, column=0, sticky="nsew")

        self.load_passwords()

    def open_credentials_popup(self, login_credential):
        if self.credentials_popup is not None and self.credentials_popup.winfo_exists():
            self.credentials_popup.focus()
            return
        
        self.credentials_popup = CredentialsPopup(
            credential_id=login_credential.id,
            domain=login_credential.domain,
            username=login_credential.associated_username,
            encrypted_password=login_credential.encrypted_pass,
            master_key=self.user.master_key,
            on_save_callback=self.load_passwords
        )
        self.credentials_popup.grab_set()

    def debounce_search(self, event=None):
        if self._search_debounce_job:
            self.after_cancel(self._search_debounce_job)
        self._search_debounce_job = self.after(300, self.load_passwords)

    def load_passwords(self):
        for widget in self.passwords_frame.winfo_children():
            widget.destroy()

        all_logins = get_login_credentials(self.user.id)

        search_term = ""
        if hasattr(self, 'search_bar'):
            search_term = self.search_bar.get().lower()

        if search_term:
            filtered_logins = [login for login in all_logins if search_term in login.domain.lower()] if all_logins else []
        else:
            filtered_logins = all_logins

        if not filtered_logins:
            if not all_logins:
                message = "No passwords saved yet."
            else:
                message = "No matching passwords found."
            no_data_label = ctk.CTkLabel(self.passwords_frame, text=message, text_color="gray50")
            no_data_label.pack(pady=10, anchor="w")
            return
            
        for login in filtered_logins:
            item_button = ctk.CTkButton(
                self.passwords_frame, 
                text=f"  {login.domain}", 
                font=ctk.CTkFont(weight="bold", size=20), 
                anchor="w",
                width=400,
                height=48,
                text_color="#262626",
                fg_color="#EDEDED",
                hover_color="#FFD9AA",
                command=lambda l=login: self.open_credentials_popup(l)
            )
            item_button.pack(anchor="w", padx=20, pady=10)
            
            arrow_label = ctk.CTkLabel(item_button, text="▶", font=ctk.CTkFont(weight="bold", size=20), text_color="#262626", bg_color="transparent", fg_color="transparent")
            arrow_label.place(relx=0.95, rely=0.5, anchor="e")

    def handle_logout(self):
        from ui.login_screen import LoginWindow
        self.destroy()
        login_win = LoginWindow()
        login_win.mainloop()

    
    def open_new_login_popup(self):
        if self.new_login_popup is not None and self.new_login_popup.winfo_exists():
            self.new_login_popup.focus()
            return

        self.new_login_popup = NewLoginPopup(
            user_id=self.user.id,
            master_key=self.user.master_key,
            on_save_callback=self.load_passwords
        )
        self.new_login_popup.grab_set()



if __name__ == "__main__":
    ctk.set_appearance_mode("light")       
    theme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'theme.json'))
    ctk.set_default_color_theme(theme_path)
    app = Dashboard()
    app.mainloop()