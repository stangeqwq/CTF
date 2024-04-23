from Crypto.Util import number
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

n =  int("00:a5:57:9e:ab:77:59:75:76:cf:e8:2c:50:36:4b:5e:be:b7:d1:7e:a8:1a:a8:a6:1e:31:05:e4:57:25:6d:89:0f:2f:a2:ae:81:ac:ed:51:ea:77:f3:d6:af:95:bc:ae:bb:b9:a2:67:c3:f6:fa:aa:f3:ca:40:7f:45:9b:64:d4:42:63:aa:7c:41:aa:fc:b9:2a:53:ec:99:22:00:c3:16:b5:18:00:c6:28:47:32:f0:4f:62:11:46:73:64:47:b8:24:2e:98:06:d6:ce:db:f9:69:0e:b1:c8:64:57:5e:4e:3f:03:6e:69:f0:ed:8f:29:3a:aa:df:0d:91:81:8f:d5:46:9c:75:dd:48:63:b3:0b:cf:65:f5:32:f0:59:80:ce:20:45:40:d5:29:f7:a4:e2:25:b2:b4:54:30:70:c1:b6:4d:a8:7a:5b:61:0f:d8:a5:fb:99:48:7f:58:49:f5:d3:d5:1f:6b:97:49:7e:0b:12:de:3d:25:6f:5f:01:0f:ce:b8:c6:dc:1a:9c:af:7c:48:8a:8a:5e:9e:e6:5c:62:5a:e0:21:28:f7:d3:13:7e:4a:cc:40:60:8a:34:d0:45:de:4f:07:06:ce:76:a5:ae:2a:2c:82:eb:a9:a2:ad:48:28:58:ae:45:51:46:fd:16:7b:81:69:ab:e4:61:f8:29:08:5b".replace(":",""), 16) # modulus
e = 0x10001  # public exponent
d = int("32:5a:af:e8:fa:6d:15:37:fc:f3:71:63:70:55:9d:e2:29:6b:34:ce:8f:67:e3:47:78:98:99:c4:ec:92:22:56:ac:a4:37:cf:28:52:12:4b:7d:02:96:d4:5c:9e:dc:fc:30:f9:c3:ee:4b:6e:65:d7:df:35:ab:4d:10:99:31:87:92:80:de:5c:c5:6d:38:1b:2a:f9:f8:5d:01:ac:68:62:f8:8f:6b:c9:e2:7d:21:f0:9b:26:35:b5:78:c9:da:cb:b2:20:fc:9c:38:dd:87:64:b6:63:f0:6a:96:ad:12:d9:5f:fb:25:6a:89:7e:bb:08:b1:f7:42:53:99:08:ab:e3:da:d4:24:12:84:08:22:60:3b:54:9b:17:0b:d8:a7:85:1e:45:89:00:7d:ca:55:9f:56:7f:df:49:e5:3f:af:8a:6f:3f:d9:1e:5b:44:34:c9:08:3a:f9:95:fb:b0:e2:9f:82:da:43:8e:ec:90:73:ee:10:a2:7d:78:32:73:a9:a1:e2:b2:47:c9:4d:4e:84:85:13:6f:50:af:e3:a7:97:fc:12:ee:ef:65:06:ba:cc:7a:ac:be:a7:a8:dc:00:34:48:ed:3d:c1:3d:c2:05:a7:d5:70:e2:d6:36:a4:b1:66:73:eb:ae:4a:5a:70:3f:ea:cd:b0:80:11:9d:28:b9:ab:91".replace(":",""),16)  # private exponent
p = int("00:d8:43:52:83:af:1f:f9:cf:eb:58:91:6d:af:3a:31:f8:42:a1:8a:d3:c0:d0:48:f0:a4:ff:fc:82:36:7d:55:b1:7e:a8:db:72:ea:1e:40:c5:e5:b5:12:8b:0e:d2:b3:c9:80:8f:7d:e2:20:72:02:ea:ca:d3:85:6a:c8:06:0d:5b:86:25:16:80:0a:2e:7e:d2:ee:29:44:59:dd:04:4f:42:fa:bd:ce:2e:87:b4:23:20:a7:53:9c:f4:56:b5:38:09:a9:f1:bd:24:78:0d:7d:c4:12:ff:fa:fd:92:74:d8:0d:0a:62:86:cb:4e:94:87:3f:6c:b8:22:7d:4f:69:d1:39".replace(":",""),16)  # prime 1
q = int("00:c3:b9:10:c4:e2:33:bd:74:85:cc:67:48:93:5f:34:c4:36:26:5f:96:f0:36:0c:1f:49:26:d1:e4:79:d6:ee:ed:d4:c0:31:3d:02:e5:c2:a8:ba:3b:8d:ee:ba:cf:d3:c3:28:a1:3f:36:99:35:ad:87:36:07:7e:90:3e:2b:a0:e4:d5:d8:16:c0:fc:e2:54:dc:b1:0b:ce:ca:78:44:aa:b0:98:85:6d:3c:e1:e1:ca:88:52:9a:b0:cb:80:e0:0d:ac:c3:2f:05:9a:a1:6e:51:bc:d6:79:e2:d4:37:8a:ff:44:85:16:56:e2:1a:ce:ec:8d:e0:9b:f2:76:a4:c9:2a:33".replace(":",""),16)  # prime 2
exp1 = int("31:85:60:fc:b4:7a:4e:fa:f4:7a:48:7a:e4:58:20:1f:28:2a:d3:9e:5f:95:92:4e:40:8a:39:a9:1b:8f:21:b3:4e:3c:9e:5b:b7:0e:8c:68:84:8c:2d:1d:d8:9c:18:fd:38:4a:23:5a:47:71:b4:07:4d:c0:97:d9:76:ca:23:fe:e4:3d:d3:e4:27:f0:b3:ab:db:4b:69:d2:66:10:d9:91:8d:d7:2e:c2:6a:e2:ad:f4:89:3c:55:41:82:25:67:1a:97:66:ba:98:02:41:9c:9d:ec:77:df:62:77:49:f8:3b:2c:38:99:83:2e:90:46:54:18:b2:25:7b:aa:56:a1:c9".replace(":",""),16)# exponent 1
exp2 = int("32:99:72:b3:63:c3:7a:94:58:4e:ea:d8:c1:78:d8:9c:6d:5f:68:51:0e:52:fa:b9:4f:e1:20:5c:4f:ff:78:0f:b6:73:e5:86:df:6b:e4:f2:58:0b:33:7b:67:82:79:3d:b8:10:4f:d6:5e:af:98:e8:1e:d8:bb:28:b1:59:f8:23:91:01:67:88:87:18:40:56:39:d3:52:a7:d7:85:f1:16:ec:a7:7a:01:46:68:68:42:ec:10:1f:ea:cc:ab:9f:fd:6d:0c:88:07:5c:fa:b7:58:f9:9d:d3:3d:88:0a:80:4a:07:9a:29:e6:14:86:30:73:d1:80:9f:a3:7a:a0:a3:2f".replace(":",""),16)  # exponent 2
coeff = int("47:04:ad:c3:04:de:24:db:5e:45:8d:9a:3a:e8:98:00:bc:89:60:2c:35:12:15:4f:96:b5:38:a2:6a:8d:15:63:9e:70:54:f7:16:fc:a4:c9:20:9f:21:df:a4:87:74:67:a3:99:d9:0e:1e:4b:fe:ac:5b:19:8b:c4:a5:d9:94:cf:e1:1c:78:1d:c4:62:3a:85:3f:b9:db:54:9d:02:9a:c7:cf:d1:94:a6:27:6a:9b:a4:92:7f:30:72:66:66:e9:a9:ea:46:3d:6e:fb:ab:87:1f:48:10:a2:95:0f:30:a5:79:fc:fb:b9:f8:c9:6d:26:b6:b1:de:49:60:15:75:58:5e".replace(":",""),16)  # coefficient

public_numbers = rsa.RSAPublicNumbers(e, n)
private_numbers = rsa.RSAPrivateNumbers(
    p=p, q=q, d=d, dmp1=exp1, dmq1=exp2, iqmp=coeff, public_numbers=public_numbers
)

private_key = private_numbers.private_key(default_backend())
public_key = public_numbers.public_key(default_backend())

# Encrypted text
encrypted_text = b'bs\x1dL\xa6\x9f+;sr\x8e*1\x04\xfe)i\x9b4\x84\xc4\xee\xe9\x15\x08\xba\xd8\xe4"\xd8\xcc\xfe\xc3\t\xbc{\x13\xfe\xf6\xd3\xa5+\xc1\x0e\xc7/2\xbe\x04f\xf3\xd8=$\x8b/\xff\x91o\xd0b\x8f\x1f\xa6\x9bY\xd1\xfa\x8f\xa1`\xd3\x9cqn\x89\x8c]+\xa2\xe6\x02\xc7\x02\xfb^m*\xa6\xa8I\xb1\x89\xa1:x.\xc9\x9e\xab\x97\x19!\xf9\xdc5\xbf\xac\xb8\xee\xb4\t\xe3\xe8\xa5\xdcY\xcc0.\xde\x91j\xeb\xdd\xc8\xe3\xb0)X\xc5\xb8\xbf63\xff\xcb\x97\x9b\x17a\xbb\x8c%\x98^\x8f\xa9\x83I\x10\x9e\xd6\x8aY\x97\x86\x84\x05m\x12\x84\xdf\x14\xb6o\x18\xc4`\x85!}\x94+ct\xd8\xd0\x9b\x07\xbabW\x86\x90\x1e\x10I\x8fP/\xad\xc3\x99-\xd1\n\xd95\x80\'\xb2izj\xd8\xc7n\xa3\t\x88D\x19\x12/\x12\xf2\xd6\xc8\x95\xa2\xc5Mt\x10\xe3\xe7\x7f\xd8SF\x18\xc79F\xf6!\x8e\xf3\xbfy\x06@\xefw\xc4:"\xe5\xb72\x1e\xe6&O\xd4'

# Decrypt with the private key
decrypted_data = private_key.decrypt(
    encrypted_text,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
# Print the decrypted data
print(decrypted_data.decode('utf-8')) #FLAGG: PST{ItsPrivateForAReason}