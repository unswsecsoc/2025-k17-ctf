The encryption scheme for this challenge is, given a plaintext `m`, we AES encrypt it to get `c` and send $(\frac1r \mod n, r^ec^e\mod n, r^dc^d\mod n)$, for some randomly generated number `r`. The third element is a "signature" which is verified, when exponentiated with $e$ and multiplied with $\frac1r$, that the result is $c$ (which can be found by decrypting the second element) and the second element is the RSA encryption. $\frac1r$ is meant as a salt. We're given a decryption for this scheme which does the verification first before decrypting (but not printing the output).

One spottable vulnerability is the AES decryption itself. We see that we try to `unpad` the message here:
```py
            return unpad(AES.new(self.aes_key, AES.MODE_CBC, iv).decrypt(ciphertext), 16)
```

We also see successful decryptions and errors are **distinguished**:
```py
        else:
            print("NAY!")
    except:
        print(f"what is bro doing 💀")
```

This is a possible setup for a [padding oracle attack](https://en.wikipedia.org/wiki/Padding_oracle_attack#Padding_oracle_attack_on_CBC_encryption).

It seems like we can't send arbitrary messages, but one key observation is that because we're given the signature, we can find the original message by raising the third element of the given tuple to the power of $e = 65537$ and then multiplying by the first element. We can then multiply the message by whatever scalar we want by simultaneously changing the salt and ciphertext to be inversely proportional to one another.

A much easier way of defeating the RSA scheme is by just sending `(c, 1, 1)` (exercise for the reader!). Now, we can perform a padding oracle attack to retrieve the original message and obtain the flag.