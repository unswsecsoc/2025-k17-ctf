from Crypto.Util.number import isPrime
from time import time

k = 1
count = 0
def numerator(a, b):
    return a**2 + b**2 + 3*a + 3*b + a*b

def denom(a, b):
    return 2 * a * b + 7

def generate(a, b, n):
    global count
    print("Generating for a and b ", a, b, "with divisor", n)
    while True:
        c = 2 * n * b - 3 - b - a
        if c < 0:
            print("nup bad")
            return
        a = c

        assert numerator(a, b) % denom(a, b) == 0
        a, b = b, a
        if a.bit_length() >= 1024:
            if isPrime(a):
                print(a, b)
                print(a.bit_length(), b.bit_length())
                return

for a in range(1, 10):
    for b in range(1, 10):
        if numerator(a, b) % denom(a, b) == 0:
            generate(a, b, numerator(a, b) // denom(a, b))