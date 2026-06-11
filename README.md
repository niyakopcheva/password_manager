# Python Secure Vault

## Overview

Python Secure Vault is a desktop password manager built on zero-knowledge security principles. It provides a secure local environment to store and manage sensitive login credentials, ensuring that only the user, with their master password, can access the encrypted data.

## Security Architecture

The application's security is built on a "zero-knowledge" principle, meaning the raw master password is never stored. Instead, it's used in a chained key derivation process to generate a key for encryption and a subsequent hash for authentication.

### 1. The Encryption Key (`master_key`)

This key is used to encrypt and decrypt the passwords in your vault. It is **never stored on disk**.

**Process:** `Master Password + vault_salt -> PBKDF2 -> master_key`

When a user registers, a unique `vault_salt` is generated. The `master_key` is derived on-the-fly by combining the master password with this `vault_salt` using the PBKDF2 key derivation function (with 600,000 iterations). This key is held in memory only for the duration of an active session and is used with the Fernet (AES-128-CBC) symmetric encryption algorithm.

### 2. The Authentication Hash (`master_pass_hash`)

This hash is used *only* to verify your identity when you log in. It is derived from the encryption key.

**Process:** `master_key + login_salt -> PBKDF2 -> master_pass_hash`

After the `master_key` is derived, it is immediately combined with a second unique salt, the `login_salt`. This combination is run through PBKDF2 again to produce the final `master_pass_hash`, which is what gets stored in the database for authentication. The `login_salt`'s purpose is to defeat Rainbow Table attacks.

## Technology Stack

-   **Language:** Python
-   **Database:** PostgreSQL
-   **GUI Framework:** CustomTkinter
-   **Cryptography:**
    -   `cryptography` (Fernet for AES-128 symmetric encryption)
    -   `hashlib` (PBKDF2-HMAC-SHA256 for key derivation)
-   **Database Driver:** `psycopg2-binary`
-   **Configuration:** `python-dotenv` for environment variable management.

## Setup

1.  **Clone the repository.**
2.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3.  **Configure Environment:** Create a `.env` file in the root directory with your PostgreSQL connection details (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`).
4.  **Run the application:**
    ```sh
    python src/main.py
    ```