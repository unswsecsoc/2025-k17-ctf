from hashlib import sha1

flag = [0x13e, 0x110, 0x134, 0x14e, 0x164, 0x152, 0x1da, 0x150, 0x16e, 0x1d0, 0x106, 0x162, 0x1d0, 0x1da, 0x156, 0x17a, 0x15c, 0x1de, 0x106, 0x16a, 0x1de, 0x106, 0x16e, 0x1d8, 0x166, 0x120, 0x142]

def a(x: int) -> int:
    return (x) ^ 0xa3

def b(x: int) -> int:
    return (x ^ 0xfe) >> 1

def c(inp: list[int])->str:
    return ''.join(chr(x) for x in [a(b(i)) for i in inp])

if __name__ == "__main__":
    print("Its simple really...you give me the right input, I give you the right flag!")

    og = b"l\x01\x02o\x03\x040\x06\x07k\xa0\x20_\x20\xf0A\x20\xa0t\xf0\x0a_\x04\x02m\x30\x503"
    x = og
    for _ in range(3):
        x = sha1(x[::3]).hexdigest().encode()
    
    print(x.decode() + '\n')

    ans = input("Input > ")
    if ans.encode() == og[::3]:
        print(c(flag))
    else:
        print("Better luck next time!")