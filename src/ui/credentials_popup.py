import customtkinter as ctk
from modules.crypto import decrypt_data


class CredentialsPopup(ctk.CTkToplevel):
    def __init__(self, domain, username, encrypted_password, master_key):
        super().__init__()

        self.title(f"Credentials for {domain}")
        self.geometry("400x275")
        self.attributes("-topmost", True)

        decrypted_password = decrypt_data(encrypted_password, master_key)

        self.domain_label = ctk.CTkLabel(self, text=f"🌐 {domain}", font=ctk.CTkFont(size=20, weight="bold"))
        self.domain_label.pack(pady=(20, 10), padx=20)

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)

        username_label = ctk.CTkLabel(main_frame, text="Username", anchor="w")
        username_label.grid(row=0, column=0, sticky="ew", padx=5)

        username_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        username_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 15))
        username_frame.grid_columnconfigure(0, weight=1)

        self.username_entry = ctk.CTkEntry(username_frame)
        self.username_entry.insert(0, username)
        self.username_entry.configure(state="readonly")
        self.username_entry.grid(row=0, column=0, sticky="ew")

        self.copy_username_btn = ctk.CTkButton(
            username_frame, text="Copy", width=70,
            fg_color="transparent", text_color=("gray14", "gray84"),
            hover_color=("gray70", "gray30"), command=self.copy_username)
        self.copy_username_btn.grid(row=0, column=1, padx=(5, 0))

        password_label = ctk.CTkLabel(main_frame, text="Password", anchor="w")
        password_label.grid(row=2, column=0, sticky="ew", padx=5)

        password_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        password_frame.grid(row=3, column=0, sticky="ew", padx=5)
        password_frame.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(password_frame, show="*")
        self.password_entry.insert(0, decrypted_password)
        self.password_entry.configure(state="readonly")
        self.password_entry.grid(row=0, column=0, sticky="ew")

        self.show_password_btn = ctk.CTkButton(
            password_frame, text="👁", width=30,
            fg_color="transparent",
            text_color=("gray14", "gray84"),
            hover_color=("gray70", "gray30"),
            command=self.toggle_password_visibility)
        self.show_password_btn.grid(row=0, column=1, padx=(5, 0))

        self.copy_password_btn = ctk.CTkButton(
            password_frame, text="Copy", width=70,
            fg_color="transparent", text_color=("gray14", "gray84"),
            hover_color=("gray70", "gray30"), command=self.copy_password)
        self.copy_password_btn.grid(row=0, column=2, padx=(5, 0))

    def _copy_to_clipboard(self, text_to_copy, button):
        self.clipboard_clear()
        self.clipboard_append(text_to_copy)
        original_text = button.cget("text")
        button.configure(text="Copied!")
        self.after(1500, lambda: button.configure(text=original_text))

    def copy_username(self):
        self._copy_to_clipboard(self.username_entry.get(), self.copy_username_btn)

    def copy_password(self):
        self._copy_to_clipboard(self.password_entry.get(), self.copy_password_btn)

    def toggle_password_visibility(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
