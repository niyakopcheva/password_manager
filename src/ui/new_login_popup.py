import customtkinter as ctk
from tkinter import messagebox
from modules.vault import add_login_credentials

class NewLoginPopup(ctk.CTkToplevel):
    def __init__(self, user_id, master_key, on_save_callback=None):
        super().__init__()

        self.user_id = user_id
        self.master_key = master_key
        self.on_save_callback = on_save_callback

        self.title("New Login")
        self.geometry("400x380")
        self.attributes("-topmost", True)

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        domain_label = ctk.CTkLabel(main_frame, text="Domain", anchor="w")
        domain_label.grid(row=0, column=0, sticky="ew", padx=5)
        self.domain_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., google.com")
        self.domain_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 15))

        username_label = ctk.CTkLabel(main_frame, text="Username", anchor="w")
        username_label.grid(row=2, column=0, sticky="ew", padx=5)
        self.username_entry = ctk.CTkEntry(main_frame, placeholder_text="Your username or email")
        self.username_entry.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 15))

        password_label = ctk.CTkLabel(main_frame, text="Password", anchor="w")
        password_label.grid(row=4, column=0, sticky="ew", padx=5)

        password_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        password_frame.grid(row=5, column=0, sticky="ew", padx=5)
        password_frame.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(password_frame, show="*", placeholder_text="Enter a strong password")
        self.password_entry.grid(row=0, column=0, sticky="ew")

        self.show_password_btn = ctk.CTkButton(
            password_frame, text="👁", width=30,
            fg_color="transparent",
            text_color=("gray14", "gray84"),
            hover_color=("gray70", "gray30"),
            command=self.toggle_password_visibility)
        self.show_password_btn.grid(row=0, column=1, padx=(5, 0))

        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.save_button = ctk.CTkButton(actions_frame, text="Save", width=150, height=40, command=self.handle_add_credentials)
        self.save_button.pack()


    def toggle_password_visibility(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def handle_add_credentials(self):
        domain = self.domain_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not all([domain, username, password]):
            messagebox.showerror("Error", "All fields are required.", parent=self)
            return

        add_login_credentials(
            user_id=self.user_id,
            domain=domain,
            username=username,
            plaintext_password=password,
            master_key=self.master_key
        )

        if self.on_save_callback:
            self.on_save_callback()

        self.destroy()
