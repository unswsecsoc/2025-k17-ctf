We're given a Paillier-encrypted flag, and a program which will "tests" us by seeing if we understand the Paillier system by allowing us to input an encrypted message, performing a "trick" on it, and then checking if we can provide an encrypted version of the message with the trick applied.

The idea is that Paillier encryption is homomorphic between two groups. tl;dr, $\mathrm{enc}(x)\cdot \mathrm{enc}(y) = \mathrm{enc}(x + y)$ (this also means $\mathrm{enc}(x)^y = \mathrm{enc}(xy)$). The tricks involve shifting/concatenating the strings, which are mathematically equivalent to multiplying the integer representations by a multiple of $256$ and adding! So it seems this system ensures we can performs "tricks" on an encrypted message, like the encrypted flag, without ever knowing what it actually is...

...except, the left shift trick, when performed on a message $\ge \frac n{256}$, will give something $\ge n$. This will ALWAYS cause our trick to fail because our decrypted message will be taken $\mod n$, while the trick is not! This gives us an oracle to determine if our message is $\ge\frac n{256}$.

If we multiply the flag (say $F$) by $2^i$ (by using the homomorphic property of Paillier by exponentiating by $2^i$) until we obtain the first $i$ where $2^{256}2^{i+1}F\ge n$ (via our oracle), then we can barely ensure $\frac n2 \le 2^{256}2^iF \le n$ (note that $2^{256}F \le n$). So, we know $2^i2^{256}F$ sits somewhere

```
0 ----------------- n / 2 ----------------- n
                      ^---------here--------^
```

and subtracting $F$ by $2^{-i-256} \frac n4\mod n$ will subtract the whole thing by $\frac n4$, which will put $2^i2^{256}(F - 2^{-i-256}\frac n4)\mod n$

```
0 ------ n / 4----- n / 2 ------- 3n / 4 -------- n
           ^-------- here -----------^
```

so we can use the oracle again to reduce the search space by $\frac12$. We can do this interval moving trick repeatedly for each $\left\lfloor\frac n{2^k}\right\rfloor$ in essentially a binary search pattern (either adding or subtracting) until we determine the position of $F \pm \mathrm{ a bunch of numbers }, and reverse out the value of $F$.