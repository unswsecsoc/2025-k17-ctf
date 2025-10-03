# ElCamel
AKA Williloo's excuse to show you very cool maths cos NUMBER THEORY IS BEAUTIFUL and if you disagree then square up behind K17 at dusk I will find you.

## Introduction
This challenge is based on the ElGamal encryption scheme...that's basically it...

Oh wait let's step through what happens in the source code:
- Import pre-determined **primes** `p`, `q`, as well as the flag
    - When `p`, `q` are printed, we can find that `p = 2q+1`: `p` is known as a *safe prime*
- We use the `findGenerator` function...keep this function in mind its sus
- We then play the game! We can control `m0`, `m1`...the rest of the game is essentially
running the `rng` function on either `m0` or `m1`, and we have to guess whether `m0` or `m1` was
the input to the rng function.
    - The `rng` functino is also sus...
- If we guess at least 38 times correctly, we win, otherwise, we lose (hint hint is 38/50 ~ 75%????)

## Number Theory Interlude
If you are a number theory enjoyer skip this section. If you don't know what a quadratic residue is, pls read on...

### Quadratic Residues
Maths people are so pretentious...a quadratic residue is just a square number modulo n, i.e. there exists
some y such that y^2^ = x mod~n~. For example, if we're working mod~7~:
| x | x^2^ |
|---|---|
|0|0|
|1|1|
|2|4|
|3|2|
|4|2|
|5|4|
|6|1|

We can see that the only QR's mod~7~ are {0, 1, 2, 4}. A nice thing about QR's is that if `x` is a QR, then `x^n` for any `n` is also a QR!
Proof is just y^2^=x => (y^n^)^2^ = x^n^. This is kinda nice! Notice that, if we exclude 0,
then there are exactly 3 Qr's  and 3 non-Qr's mod~7~! In general, there are (p-1)/2 QR's and non Qr's!

A nice property of QR's: if `x` is a QR, then x^(p-1)/2^=1....source: trust me bro...If you want, look up Euler's criterion...its a whole can of worms...
Hopefully this is starting to look a bit sus to you if you recall the `findGenerator` functions....

### Orders
![](order.png)

Wtf is order??? The order of an element `g` in {0, 1, 2...p-1} is the smallest `k` such that g^k^=1 mod~p~.
Let's look at an example with p=7:

| g | g^1^ | g^2^ | g^3^ | g^4^ | g^5^ | g^6^ | order |
|---|---|---|---|---|---|---|---|
|1|1|1|1|1|1|1|1|
|2|2|4|1|2|4|1|3|
|3|3|2|6|4|5|1|6|
|4|4|2|1|4|2|1|3|
|5|5|4|6|2|3|1|6|
|6|6|1|6|1|6|1|2|

A nice observation we can make is that if `q|p-1`, then g^(p-1)/q^ != 1 => order(g^(p-1)/q^) = q. This is provable
but you gotta trust me on this one man...just look at the examples and trust...!

Wait so what are generators...a generator `g` is basically some number such that, when we power it and
get {g, g^2^, g^3^...} it will generate some set of values. For example, `3` is a generator for the set
{1, 2, 3, 4, 5, 6} mod~7~...see the table for proof...

## Back to the Code
There's a few suspicious things about this code. We'll start with `findGenerator`:
```
def findGenerator():
    while True:
        h = randbelow(p)
        if pow(h, q, p) != 1:
            continue

        g = pow(h, 2, p)
        if g != 1:
            return g
```
Recalling that `p=2q+1`, we essentially have:
1. h is a QR
2. g has order `q`

This basically means that `g` is generator for all the QR's mod~p~!

Now let's look at the `rng` function...
```
def rng(key):
    r = randbelow(p)
    
    c = pow(g, r * x, p)
    c += key

    return c % p
```

This is a TERRIBLE rng function...even though we choose a random number `r`, essentially all we're doing
is (g^r^)^x^...the result is still a QR because `g` is a QR...

We then add the `key`, which remember is just `m0` or `m1`, onto this power of `g`, and the result mod~p~ is
our random number...this is definitely exploitable...

### EXPLOIT TIME
To win, we basically only need a 75% success rate. If we send `m0` = 0 and `m1` = 1, we can guarantee that
`rng(m0)` is a QR!!!! Why? Because `rng(0)` = (g^r^)^x^ mod~p~, which we know is a QR! This means that if 
our `rng` function is NOT a QR, then the input is 100% `m1`!!!!

As for when `rng` is a QR...we can't really tell if it's `m0` or `m1`...so just guess it was `m0` as the input ;P...

Looking at our final probability for this method:
- If `m0` was the input, we are 100% right: `rng(m0)` is always a QR, and whenever we see output is a QR, we 
guess `m0`
- If `m1` was the input, we are 50% right: `rng(m1)` has a 50-50 chance of being a QR or not (distribution of QRs is roughly
uniform...) Half the time, we get `rng(m1)` is a QR, in which case we guess wrong, the other half of the time
we get `rng(m1)` is not a QR, in which case we are always right.

Overall, our success rate is 0.5\*100% + 0.5\*50% = 75%: we have a pretty decent chance of winning if we play the game 5 times!!!
Remember that to test if a number is a QR, we can just check if c^q^ = 1 mod~p~, where q=(p-1)/2!

# Payload
```
from pwn import *

def solve(p, q, c):
    ## Check if c is QR
    return pow(c, q, p) == 1

r = remote("challenge.secso.cc", 7001)

r.recvuntil(b'\n')
r.recvuntil(b'\n')
r.recvuntil(b'\n')

p = int(r.recvuntil(b'\n').strip().decode())
q = int(r.recvuntil(b'\n').strip().decode())

r.sendline(b"0")
r.sendline(b"1")

r.recvuntil(b"How long do you want the coin to be?> ")

for _ in range(50):
    c = int(r.recvline().strip())

    r.recvuntil(b"(H or T)> ")

    if solve(p, q, c):
        r.sendline(b"H")
    else:
        r.sendline(b"T")

    res = r.recvuntil(b"\n\n")
    print(res)

print(r.recv())
```