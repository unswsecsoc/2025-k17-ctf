We have to provide two numbers, a, b, which are used to generate a secret key `d` in an RSA system. Being able to choose `d` is already very suspicious. If it's something predictable, then obviously we can break everything, however:
- `a` and `b` must be 1024-bit numbers, and `a` must be prime (the check is (purposefully :P) broken in that `b` doesn't have to be prime (in fact it shouldn't :PPP))
- `d` is calculated as:
```py

phi = (p - 1) * (q - 1)


# to harden d
r = ((a**2 + b**2 + 3*a + 3*b + a*b) * pow(2 * a * b + 7, -1, phi)) % phi
while gcd(k := int.from_bytes(urandom(32), "big"), phi) != 1:
    continue

d = pow(k, r, phi)
```

This is a rational function taken under a modulus of `phi` (which is $\varphi(n)$, i.e. via the totient function). Since $\varphi(n)$ cannot be calculated without knowing the factorisation of $n$ (and in fact $r$ won't even behave nicely since it's not taken under mod $\varphi(\varphi(n))$ ), we need a different approach.

If `r` is a very small number, then it's possible that `d = k^r` will also be small - this leads us to another attack path: the Wiener attack, which allows you to recover ciphertexts when $\log(d) < \frac {\log(n)}4$ (i.e. less than a quarter of the bits).

A key point to note that this rational function is symmetric in `a` and `b`, so we can potentially generate very large values of `d` whose rational function, without taking any mod, give us a very small integer number - we may be able to generate these via Vieta jumping! [This](generate_large_a_and_b.py) should do this.

This quickly gives us a prime/non-prime pair that satisfies the constraints and, upon plugging into the calculation of `r`, will always give `2`. This means we will take $d = k^2$. Since $k$ is $32 \times 8 = 256$ bits, $d$ will be $512$ bits, while $n$ (and thus $\varphi(n)$) will be $1024\times1024 = 2048$ bits, which is plenty of leeway for the Wiener attack.