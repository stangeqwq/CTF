ct = "8e7e24751f22bf36361a14f243beb4011469f9764108770874d5e7e0e1656d5e13b1f75a12ee8c972fbc1c31a2ac18b4f4088c5d3a61e2a204ebc1978cadcfa2786bec26f43480a796299a18ac57baf1b8b809af387cdc3f55420a479950351a4bd7da21a3ef6e53ac26c1ee43845f19b21e37775b8bf09b4bf5d220bb888a3d38fc280c972b837a107d98bb5aa1c41f43f6aa73ddd0f73bf16a9f5a41885aff4c4d230c2b22442225dc4a09d5c317d13946f447cd122b207c22c23092a0aa593258e20e978b573c3e6acea22d4ffb3db6d9ddcfc24f1db4fa966240c664631c6de34bb67c2da7b18bd1fd53b45875b06f99c144fa7a866c15dc3ea46b694685d03c07392d0a8a1b063d339724838c64102dd64e7a366d4153d5d9eadb64784e01a6cd266dc4909d30fd1839a7b709befd22"
ct = bytes.fromhex(ct)
shakespeare = open("shakespeare.txt","rb").read()[0:16*16]
flag = b"flag{custom_AE_S-CTR_with_a_reu"
pt = shakespeare + b"\n\n" + flag

second_ct = ""
solution = ""
def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


for i in range(0, len(ct), 16):
    second_ct += xor(pt[i:i+16], ct[i:i+16]).hex()

second_ct = bytes.fromhex(second_ct)
second_ct[0:16]

# we can xor (ct encrypted to the end of ciphertext to get the flag from plaintext since ct used repeats long_to_bytes((i//16)%16,4))
# see below
for i in range(0, len(ct), 16):
    print((i//16)%16) # repeating pad

for i in range(0, len(second_ct), 16):
    solution += xor(second_ct[16*2:16*3], ct[i:i+16]).hex()

# flag{custom_AE_S-CTR_with_a_reuse_vulnerability}
print(bytes.fromhex(solution))

"""
b"THE SONNETS\n\nby William Shakespeare\n\nFrom
 fairest creatures we desire increase,\nThat thereby beauty's rose
   might never die,\nBut as the riper should by time decease,\nHis tender
     heir might bear his memory:\nBut thou contracted to thine own bright 
     eyes,\nFeed's\n\n
     flag{}
"""