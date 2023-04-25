import os

# Prompt the user for input values
filename = input("Enter the name of the file to encrypt: ")
usernames = input("Enter the usernames of the users who need access to the file, separated by commas: ")
passwords = input("Enter the passwords for the users, separated by commas: ")

# Split the usernames and passwords into lists
usernames = usernames.split(",")
passwords = passwords.split(",")

# Check if the file exists
if not os.path.exists(filename):
    print(f"File {filename} does not exist.")
    exit()

# Generate -K and -iv values
key = os.popen('openssl rand -hex 32').read().strip()
iv = os.popen('openssl rand -hex 16').read().strip()

# Encrypt file
encrypted_file = f'{filename}.cbc'
os.system(f'openssl aes-256-cbc -e -K {key} -iv {iv} -in {filename} -out {encrypted_file}')

# Create temp.txt and populate with user info
temp_file = 'temp.txt'
with open(temp_file, 'w') as f:
    for i, username in enumerate(usernames):
        password = passwords[i]
        f.write(f'User: {username}\n')
        f.write(f'File: {encrypted_file}\n')
        f.write(f'Command: openssl aes-256-cbc -d -pbkdf2 -a -in {encrypted_file} -out {filename} && echo "Decryption successful!" || echo "Decryption failed."\n')
        encrypted_key = os.popen(f'echo "{password}" | openssl aes-256-cbc -e -pbkdf2 -a').read().strip()
        f.write(f'Encrypted key for {username}:\n')
        f.write(f'{encrypted_key}\n')
        f.write('\n')

# Write encrypted keys to encrypted_keys.txt
keys_file = 'encrypted_keys.txt'
with open(keys_file, 'a') as f:
    for i, username in enumerate(usernames):
        encrypted_key = os.popen(f'echo "{passwords[i]}" | openssl aes-256-cbc -e -pbkdf2 -a -in {temp_file}').read().strip()
        f.write(f'User: {username}\n')
        f.write(f'File: {encrypted_file}\n')
        f.write(f'Encrypted key:\n{encrypted_key}\n')
        f.write('\n')

# Clean up unencrypted files
os.remove(temp_file)
os.remove(filename)
