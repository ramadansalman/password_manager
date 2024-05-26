from cryptography.fernet import Fernet
import json
import os

# Anahtar üretimi ve dosyaya kaydedilmesi
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Anahtarın yüklenmesi
def load_key():
    return open("key.key", "rb").read()

# Şifreleme işlemi
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Şifre çözme işlemi
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Şifre ekleme ve saklama
def add_password(site, username, password, key):
    encrypted_password = encrypt_password(password, key)
    password_data = { "site": site, "username": username, "password": encrypted_password.decode() }
    
    passwords = load_passwords()
    passwords.append(password_data)
    save_passwords(passwords)

# Şifreleri dosyadan yükleme
def load_passwords():
    try:
        with open("passwords.json", "r") as password_file:
            passwords = json.load(password_file)
    except (FileNotFoundError, json.JSONDecodeError):
        passwords = []
    return passwords

# Şifreleri dosyaya kaydetme
def save_passwords(passwords):
    with open("passwords.json", "w") as password_file:
        json.dump(passwords, password_file, indent=4)

# Şifreleri listeleme
def list_passwords(key):
    passwords = load_passwords()
    for idx, password_data in enumerate(passwords, start=1):
        decrypted_password = decrypt_password(password_data["password"].encode(), key)
        print(f"{idx}. Site: {password_data['site']}, Username: {password_data['username']}, Password: {decrypted_password}")

# Şifre güncelleme
def update_password(index, site, username, password, key):
    passwords = load_passwords()
    if 0 <= index < len(passwords):
        encrypted_password = encrypt_password(password, key)
        passwords[index] = { "site": site, "username": username, "password": encrypted_password.decode() }
        save_passwords(passwords)
        print("Password updated successfully.")
    else:
        print("Invalid index.")

# Şifre silme
def delete_password(index):
    passwords = load_passwords()
    if 0 <= index < len(passwords):
        passwords.pop(index)
        save_passwords(passwords)
        print("Password deleted successfully.")
    else:
        print("Invalid index.")

def main():
    if not os.path.exists("key.key"):
        generate_key()
    key = load_key()

    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. List Passwords")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            site = input("Enter the site: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            add_password(site, username, password, key)
        elif choice == "2":
            list_passwords(key)
        elif choice == "3":
            index = int(input("Enter the index of the password to update: ")) - 1
            site = input("Enter the new site: ")
            username = input("Enter the new username: ")
            password = input("Enter the new password: ")
            update_password(index, site, username, password, key)
        elif choice == "4":
            index = int(input("Enter the index of the password to delete: ")) - 1
            delete_password(index)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
