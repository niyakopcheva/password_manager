### PYTHON PASSWORD MANAGER DOCUMENTATION

## DATABASE

The database is a relational PostgresSQL database. It consists of only 2 tables - **users** and **passwords**

`users(id, username, master_pass_hash, login_salt, vault_salt)`
`passwords(id, user_id, domain, associated_username, encrypted_pass)`

## SECURITY ARCHITECTURE

The application's security is built on a "zero-knowledge" principle, meaning the raw master password is never stored. Instead, it's used in a chained key derivation process to generate a key for encryption and a subsequent hash for authentication.

### 1. The Encryption Key (`master_key`)
This key is used to encrypt and decrypt the passwords in your vault. It is **never stored** on disk.

**Process:** `Master Password + vault_salt -> PBKDF2 -> master_key`

- When you register, a unique `vault_salt` is generated.
- The `master_key` is derived on-the-fly by combining your master password with this `vault_salt` using the PBKDF2 key derivation function.
- This key is held in memory only for the duration of your session and is used with the Fernet symmetric encryption algorithm.

### 2. The Authentication Hash (`master_pass_hash`)
This hash is used only to verify your identity when you log in. It is derived from the encryption key.

**Process:** `master_key + login_salt -> PBKDF2 -> master_pass_hash`

- After the `master_key` is derived, it is immediately combined with a second, completely independent `login_salt`.
- This combination is run through PBKDF2 again to produce the final `master_pass_hash`, which is what gets stored in the `users` table for authentication.
- The `login_salt`'s purpose is to defeat **Rainbow Table** attacks. It ensures that even if two users have the same master password, their stored hashes will be completely different.

### Why is this Chained Derivation Secure?
Imagine a hacker breaches the database. They will have access to `master_pass_hash`, `login_salt`, and `vault_salt`.

To decrypt your passwords, they need the `master_key`. To get the `master_key`, they need your original master password to combine with the `vault_salt`.

Because PBKDF2 is a one-way function, the attacker cannot reverse the process to get the `master_key` from the `master_pass_hash` and `login_salt`. They are forced to attack the original master password. This chained process ensures that even if a weakness were found in one of the derivation steps, the other provides an additional layer of security. The attacker must still brute-force the original master password to gain access to the vault.

## USER FLOW & UI FUNCTIONALITY

The user interface is simple and intuitive, guiding the user through secure password management.

### Registration & Login
- **Registration**: A new user provides a username and a strong master password. The system handles the generation of salts and the `master_pass_hash` in the background.
- **Login**: The user enters their credentials. The application fetches the user's salts, re-derives the login hash from the provided password, and compares it to the one in the database. If they match, the `master_key` for encryption is derived and stored in memory for the session, and the user is taken to the dashboard.

### Dashboard
The central hub of the application.
- **Credential List**: Displays a clean, scrollable list of all saved credentials, identified by their domain name.
- **Search**: A search bar at the top allows the user to filter the credential list in real-time by typing a domain name. The search is "debounced," meaning it waits for the user to pause typing before querying, ensuring a smooth experience and preventing excessive database calls.
- **Add New Credential**: A prominent `+ New` button opens a popup form to add a new password entry.
- **Logout**: A button in the sidebar securely ends the session.

### Credentials Popup (View/Edit)
This popup appears when a user clicks on a credential in the dashboard list.
- **Display**: Shows the domain, username, and the password (masked by default with `*****`).
- **Actions**:
    - **Toggle Visibility**: An "eye" icon allows the user to reveal or hide the password.
    - **Copy**: "Copy" buttons next to the username and password fields allow for one-click copying to the clipboard.
    - **Edit/Save**: An "Edit" button makes the username and password fields editable and transforms into a "Save" button. Clicking "Save" updates the entry in the database, refreshes the dashboard list, and closes the popup.
    - **Delete**: A "Delete" button allows the user to permanently remove the credential from their vault.

### New Login Popup (Add)
- A straightforward form with fields for Domain, Username, and Password.
- Upon saving, the password is encrypted with the session's `master_key`, stored in the database, and the dashboard list is automatically refreshed.
