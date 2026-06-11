import os
import customtkinter as ctk
from modules.db import init_db
from ui.login_screen import LoginWindow


def main():
    # Initialize Database
    init_db()

    # Configure UI 
    ctk.set_appearance_mode("light")
    theme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui', 'theme.json'))
    ctk.set_default_color_theme(theme_path)

    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()