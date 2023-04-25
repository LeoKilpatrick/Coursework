import subprocess
import getpass

# Ask user for username, password, and filename
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")
filename = input("Enter filename: ")

# Calculate the hmac of the un-encrypted file and save to hmac.txt
command = f"openssl dgst -sha256 -hmac '{password}' {filename}"
output = subprocess.check_output(command, shell=True)
with open("hmac.txt", "wb") as f:
    f.write(output)

# Create new file called hmacs.txt and save the output of the previous command to this file
with open("hmacs.txt", "wb") as f:
    subprocess.call(command, shell=True, stdout=f)

# Create new file called temp.txt and save the command used to generate the hmac to this file
with open("temp.txt", "w") as f:
    f.write(command)

# Encrypt temp.txt using the user's password
command = f"openssl aes-256-cbc -e -pbkdf2 -a -in temp.txt -out temp.txt.enc -pass pass:{password}"
subprocess.call(command, shell=True)

# Add encrypted key to encrypted_hmac.txt
with open("temp.txt.enc", "rb") as f:
    encrypted_key = f.read()
with open("encrypted_hmac.txt", "a") as f:
    f.write(f"User: {username}\n")
    f.write(f"File: {filename}\n")
    f.write("Encrypted key:\n")
    f.write(encrypted_key.decode() + "\n")

# Repeat steps 4, 5 and 6 for all users requiring write access
while True:
    next_user = input("Enter username for next user requiring write access (or 'done' to finish): ")
    if next_user.lower() == 'done':
        break
    next_password = getpass.getpass(f"Enter password for {next_user}: ")
    
    # Encrypt temp.txt using the user's password
    command = f"openssl aes-256-cbc -e -pbkdf2 -a -in temp.txt -out temp.txt.enc -pass pass:{next_password}"
    subprocess.call(command, shell=True)

    # Add encrypted key to encrypted_hmac.txt
    with open("temp.txt.enc", "rb") as f:
        encrypted_key = f.read()
    with open("encrypted_hmac.txt", "a") as f:
        f.write(f"User: {next_user}\n")
        f.write(f"File: {filename}\n")
        f.write("Encrypted key:\n")
        f.write(encrypted_key.decode() + "\n")

# Delete temp.txt
subprocess.call("rm temp.txt*", shell=True)
