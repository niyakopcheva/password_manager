### PYTHON PASSWORD MANAGER DOCUMENTATION

## DATABASE

The database is a relational PostgresSQL database. It consists of only 2 tables - **users** and **passwords**

- # users(id, username, master_pass_hash, login_salt, vault_salt)
We store a hash of the master password, because a hash is only one-way, it cannot be reversed. When a user logs in, we hash the password input and check if that hash is the same as the one in the database. If it is, then the passwords match and we log in the user. 

For better security, we use two unique salts: a *login_salt* and a *vault_salt*.

The login salt is created when the user first registers and combined with the Master Password before hashing. While it is stored in plain sight within the database, its job is to defeat **Rainbow Table** attacks (pre-computed lists of common password hashes). It ensures that even if two users choose the exact same Master Password, their stored hashes will look completely different, forcing a hacker to brute-force your specific account completely from scratch.

To prevent a hacker from using a stolen login hash as a shortcut to cracking your encrypted data, we introduce a completely independent *vault_salt*. Python takes the Master Password, combines it with this second salt, and runs it through a computationally heavy Key Derivation Function (KDF) to generate the actual Fernet encryption key. Because the hacker has to solve an entirely separate mathematical puzzle to derive this key, cracking the login hash grants them zero advantage in unlocking the password vault.

