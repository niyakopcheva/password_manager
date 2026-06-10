import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from modules.vault import get_login_credentials

class Dashboard(ctk.CTk):
    def __init__(self, user):
        super().__init__()

        self.user = user
        self.title(f"Secure Vault - {self.user.username}")
        self.geometry("1280x720")

        # Layout config
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Secure\nVault", font=ctk.CTkFont(size=20, weight="bold"), justify="left", anchor="w")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.logout_button = ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.handle_logout)
        self.logout_button.grid(row=10, column=0, padx=20, pady=20, sticky="s")

        # Main
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.welcome_label = ctk.CTkLabel(self.main_content, text=f"{self.user.username}'s Vault", font=ctk.CTkFont(size=32, weight="bold"))
        self.welcome_label.pack(pady=20, anchor="w")

        self.passwords_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        self.passwords_frame.pack(fill="both", expand=True)

        self.load_passwords()

    def load_passwords(self):
        logins = get_login_credentials(self.user.id)
        if not logins:
            no_data_label = ctk.CTkLabel(self.passwords_frame, text="No passwords saved yet.", text_color="gray50")
            no_data_label.pack(pady=10, anchor="w")
            return
            
        for login in logins:
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
            )
            item_button.pack(anchor="w", padx=20, pady=10)
            
            arrow_label = ctk.CTkLabel(item_button, text=">", font=ctk.CTkFont(weight="bold", size=20), text_color="#262626", bg_color="transparent", fg_color="transparent")
            arrow_label.place(relx=0.95, rely=0.5, anchor="e")

    def handle_logout(self):
        from ui.login_screen import LoginWindow
        self.destroy()
        login_win = LoginWindow()
        login_win.mainloop()


if __name__ == "__main__":
    ctk.set_appearance_mode("system")       
    theme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'theme.json'))
    ctk.set_default_color_theme(theme_path)
    app = Dashboard()
    app.mainloop()