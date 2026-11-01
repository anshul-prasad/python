from cryptography.fernet import Fernet

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
# write_key()

def load_key():
    with open("key.key", "rb") as key_file:
        key = key_file.read()
        return key

key = load_key()
fer = Fernet(key)

def add():
    name = input("Account Name: ")
    pwd = input("Password: ")
    with open("passwords.txt", "a") as f:
        f.write(name + "|" + str(fer.encrypt(pwd.encode()).decode()) + "\n")

def view():
    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            name, pwd = line.split("|")
            print(f"account name: {name}, password: {fer.decrypt(pwd.encode()).decode()}")

while True:
    mode = input("Would you like to add a new password or view existing ones (view or add or quit): ")
    if mode == "q":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue