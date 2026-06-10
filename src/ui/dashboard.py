import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk

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