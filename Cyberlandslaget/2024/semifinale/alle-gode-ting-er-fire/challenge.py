from Crypto.Util.number import bytes_to_long, getPrime
from sage.all import QuaternionAlgebra, QQ, four_squares
from sympy import factorint
#from secret import FLAG


FLAG = b"flag{this_is_just_a_tes}"
# Quaternion algebra over the rational numbers, i^2 = -1 and j^2 = -1
Q = QuaternionAlgebra(QQ, -1, -1)
p = getPrime(64)
assert len(FLAG) % 4 == 0

step = len(FLAG) // 4
flag_parts = [FLAG[i : i + step] for i in range(0, len(FLAG), step)]
flag_parts = [bytes_to_long(part) for part in flag_parts]
#print(flag_parts)
flag_quaternion = Q(flag_parts)
p_quaternion = Q(four_squares(QQ(p)))
#print(p_quaternion)

x = flag_quaternion * p_quaternion

with open("output2.txt", "w") as fout:
    fout.write(f"{x = }\n")
    fout.write(f"p = {p}\n")
    fout.write(f"p_q = {p_quaternion}\n")
    fout.write(f"x_1 = {factorint(x[0])}\n")
    fout.write(f"x_2 = {factorint(x[1])}\n")
    fout.write(f"x_3 = {factorint(x[2])}\n")
    fout.write(f"x_4 = {factorint(x[3])}\n")