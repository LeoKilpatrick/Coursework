import os

# Prompt the user for input values
filename = input("Enter the name of the file to encrypt: ")
username = input("Enter the username of the user who needs access to the file: ")
password = input("Enter the password for the user: ")

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
    f.write(f'User: {username}\n')
    f.write(f'File: {encrypted_file}\n')
    f.write(f'Command: openssl aes-256-cbc -d -pbkdf2 -a -in {encrypted_file} -out {filename} && echo "Decryption successful!" || echo "Decryption failed."\n')

# Encrypt temp.txt with user's password
encrypted_key = os.popen(f'echo "{password}" | openssl aes-256-cbc -e -pbkdf2 -a -in {temp_file}').read().strip()

# Write encrypted key to encrypted_keys.txt
keys_file = 'encrypted_keys.txt'
with open(keys_file, 'a') as f:
    f.write(f'User: {username}\n')
    f.write(f'File: {encrypted_file}\n')
    f.write('Encrypted key:\n')
    f.write(f'{encrypted_key}\n')

# Clean up unencrypted files
os.remove(temp_file)

print("Encryption successful!")
