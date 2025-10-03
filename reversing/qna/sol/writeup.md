We compiled this challenge using Nuitka!!! Which is kinda notorious for being a bit hard to reverse...! That's probably why the binary is a bit cursed...
Oh yeah did I mention...we also made it statically linked so like EVERYTHING is in the binary...

Just by running the program, the output looks suspiciously like a hash, and repeating it a couple of times seems like its always the same hash output, meaning
the program is probably deterministic. 

If you run it through ltrace with `ltrace -o out.log ./chall.bin`, and search for the hash in the output...you'll get nothing. This is because the
hash is too long lol. If you just look for the first part of the hash, like `aaa57b430`, you'll actually find a series of hash looking strings, all the
way until `lo0k_At_m3`. Trying this as the password, you'll receive the flag.