def a(x):
    return x + 5

def b(x):
    return x * 67

def c(x):
    return x % 100

def d(x):
    return x % 2 == 0

def e(x):
    return x // 4

def f(x, y):
    return x % y

def gyldig(tall):
    tall = int(tall)

    return c(f(b(a(tall)), e(tall))) == 13 and d(tall)

tall = 5
while (not gyldig(tall)):
    tall += 1
print(tall)


#flag{v1rk3r_50m_0m_du_k4n_

def gyldig2(verdi):
    a = 0
    b = 0
    for c in verdi:
        if c == '9':
            return False

        if c.isupper():
            a += 1
        
        b += ord(c)

        if c == 'a':
            return False
    print(b)
    print(a)
    print(len(verdi))
    return a == 5 and b == 500 and len(verdi) == 10

verdi = ["A","A","A","A","A","#","#","#","#","#"]

gyldig2(verdi)


#flag{v1rk3r_50m_0m_du_k4n_

import base64

def gyldig3(verdi):
    a = base64.b64decode(verdi).decode("ascii")
    b = a[0:5] + a[-5:-3]
    c = a[7:-10]
    d = a[6] + c[:2] + b
    print(d)
    return d == "hei sveis!"

verdi = base64.b64encode(b" svei5hei2109876s!321")
print(verdi)
print(gyldig3(verdi))

#flag{v1rk3r_50m_0m_du_k4n_py7h0n}