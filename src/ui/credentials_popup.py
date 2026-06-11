import customtkinter as ctk
from modules.crypto import decrypt_data
from modules.vault import update_login_credentials

class CredentialsPopup(ctk.CTkToplevel):
    def __init__(self, credential_id, domain, username, encrypted_password, master_key, on_save_callback=None):
        super().__init__()

        self.credential_id = credential_id
        self.master_key = master_key
        self.domain = domain
        self.on_save_callback = on_save_callback

        self.title(f"Credentials for {domain}")
        self.geometry("400x325")
        self.attributes("-topmost", True)

        decrypted_password = decrypt_data(encrypted_password, master_key)

        self.domain_label = ctk.CTkLabel(self, text=f"🌐 {self.domain}", font=ctk.CTkFont(size=20, weight="bold"))
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

        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.edit_save_button = ctk.CTkButton(actions_frame, text="Edit", width=100, command=self.toggle_edit_mode)
        self.edit_save_button.pack(side="left")

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

    def toggle_edit_mode(self):
        if self.edit_save_button.cget("text") == "Edit":
            self.username_entry.configure(state="normal")
            self.password_entry.configure(state="normal")
            self.edit_save_button.configure(text="Save")
        else:
            self.save_changes()

    def save_changes(self):
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()

        update_login_credentials(
            credential_id=self.credential_id,
            domain=self.domain,
            username=new_username,
            plaintext_password=new_password,
            master_key=self.master_key
        )

        # Trigger the dashboard refresh
        if self.on_save_callback:
            self.on_save_callback()

        # Briefly show "Saved!" and then close the popup.
        self.edit_save_button.configure(text="Saved!", state="disabled")
        self.after(1000, self.destroy)
