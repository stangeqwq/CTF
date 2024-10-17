from pwn import *
import base64

# Set up the connection to the remote process
r = remote('pwn-intro-pwn-intro.challs.cyberlandslaget.no', 31337)

# Receive the Base64 encoded binary data
encoded_data = r.recvuntil('[yes/no]').strip()

# Decode the Base64 data
print(encoded_data.decode())
r.sendline(b'yes')

r.recvline()
encoded_data = r.recvuntil('==').strip()

encoded_data = encoded_data[12:]
print(encoded_data.decode())
decoded_data = base64.b64decode(encoded_data)
# Save the decoded data to a temporary file
with open('temp_binary', 'wb') as f:
    f.write(decoded_data)

# Make the temporary file executable
os.chmod('temp_binary', 0o755)

# Run the binary using pwntools
proc = process(['qemu-arm','./temp_binary'])

# Capture output
output = proc.recvall()

# Print the output
print("Output:")
print(output.decode('utf-8'))

# Close the process
proc.close()

# Remember to close the connection when done
r.close()
