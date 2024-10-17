from Crypto.Util.number import long_to_bytes
from sage.all import inverse_mod
from sympy import isprime
from Crypto.Util.number import bytes_to_long, getPrime
from sage.all import QuaternionAlgebra, QQ, four_squares
from sympy import factorint


Q = QuaternionAlgebra(QQ, -1, -1)
p = 9333319125218940139 # test: 17671447715245745353
x_i = [-584210810594046517355452820113415197, 487268406469160255588161824266067879, -604670429592815531484994554730642919, 523176388428119814691754655613320989]
x_test = [-2101558582212515977353, 1903871752128388316161, -2101705357768746652361, 1849281251423303287215]
x = Q(x_i)


print(x * x.conjugate())
#print(x * x.conjugate()/(x_i[0]**2+x_i[1]**2+x_i[2]**2+x_i[3]**2))
# x^2 = f^2 * p^2
print(factorint(x * x.conjugate()))

for i in range(2**4):
    p = 17852010398400078143
    p_quaternion = Q(four_squares(QQ(p)))
            #print(p_quaternion)
            # Assume x (flag_quaternion) and p are given
            # Compute the inverse of p in the quaternion algebra Q
            #print(p_quaternion)

    p_quaternion_conjugate = p_quaternion.conjugate()
            #print(p_quaternion_conjugate)

            # Compute the inverse of p_quaternion
    p_quaternion_inverse = p_quaternion_conjugate / p
            #print(p_quaternion_inverse)

    inverse_x = x * p_quaternion_inverse
            #print(inverse_x)

            # Convert the inverse quaternion back to flag parts (list of long integers)
    flag_parts_inverse = [abs(int(inverse_x[i])) for i in range(4)]
            #print(flag_parts_inverse)

            # Convert each long integer back to bytes and concatenate to obtain the flag
    recovered_flag = b"".join(long_to_bytes(part) for part in flag_parts_inverse)
    #print(f"hex = {recovered_flag.hex()}")
    #print(f"int = {int(recovered_flag.hex(), 16)}")
    #print(f"flag(decoded with p guess)={recovered_flag}")
    if b"flag" in recovered_flag:
        print(recovered_flag)
        print(p)
        break
    else: 
        print(i)
        continue
