reading_payload = """li $v0, 12
syscall
move $tX, $v0

li $v0, 12
syscall
sll $tX, $tX, 8
add $tX, $tX, $v0

li $v0, 12
syscall
sll $tX, $tX, 8
add $tX, $tX, $v0

li $v0, 12
syscall
sll $tX, $tX, 8
add $tX, $tX, $v0

"""

output_vector = "0001110111110101001101110000000110111110100010010000100000100001101001011011100100100011101111101110010101101111100100111000010101111000010001010011111000001100100110111100000010001110101010010111110100101011100001001111010101100110000001010110010011110100"
output_vector = list(map(int, output_vector))
matrix = []
with open("matrix.txt") as f:
    for line in f:
        matrix.append(list(map(int, line.split(","))))

f = open("flag_checker.s", "w")
print = lambda line : f.write(line + "\n") # ewwww

print("main:")

for i in range(8):
    print(reading_payload.replace("X", str(i)))

# Debugging read single integer
# print("li $v0, 5")
# print("syscall")
# print("move $t0, $v0")

# Debugging read second integer for add
# print("li $v0, 5")
# print("syscall")
# print("move $t1, $v0")

print(f"li $s0, {2**31}")

def easy_apply_not(rop): # not one more time, but when we know $s2 is either 0 or 1, so we just do 1 >> ($s2)
    print("srl $s3, $s0, 31")
    print(f"srlv {rop}, $s3, {rop}")

def apply_not(rop): # the right hand shift argument is applied mod 2^32, so for a true not we need to check every 5 bit chunk
    print(f"srl $s3, $s0, 31")

    for _ in range(6):
        print(f"srlv $s3, $s3, {rop}")
        print(f"srl {rop}, {rop}, 5")

    print(f"srlv {rop}, $s3, {rop}") # after 6 times, for example, 2^31 -> 2^1, so we just shift right one more time to check the top two bits

def add(target, op1, op2):
    print(f"srlv $s5, {op2}, {op1}")
    print(f"srlv $s4, {op1}, {op2}")
    easy_apply_not("$s5")
    print(f"srlv {target}, $s5, $s4")
    easy_apply_not(target)

def extract(rop, reg, i):
    print(f"srl $a1, {reg}, 0")
    if i >= 5:
        print(f"srl $a1, $a1, {i - 4}") # move to bit 4
        i = 4
    print("srl $s1, $s0, 0")
    for j in range(5 - i):
        shift = 2**(4 - j)
        print(f"srl $s2, $s1, {shift}")
        print(f"srlv $s2, $s2, $a1")
        apply_not("$s2")
        if j == 4 - i:
            break
        easy_apply_not("$s2")
        for _ in range(shift):
            print("srlv $s1, $s1, $s2")

    print(f"srl {rop}, $s2, 0")

# Debugging bit extraction from single integer
# extract("$t0", "$t0", 0)

# Debugging adding two one bit integers
# add("$t2", "$t1", "$t0")

print("srl $a0, $s0, 31")

for i, line in enumerate(matrix):
    print("srl $t8, $0, 0")
    for reg in range(8):
        for bit in range(32):
            if line[reg * 32 + bit]:
                extract("$t9", f"$t{reg}", 31-bit)
                add("$t8", "$t8", "$t9")
    print(f"srl $t9, {output_vector[i]}, 0")


    add("$t8", "$t8", "$t9") # just add actual to 1 so we get 0 if we're equal, so then we can AND (negating this again) with $v0  
    

    # now we do a AND neg b with a0, taking b to be t8 -> since t8 is already the negation of an equality matching (which is XOR), negating again will require a0 (previous runs of XORs being equal) and current XOR
    print("srlv $a0, $a0, $t8")
    # early break allows partial validating :D
    # if i == 10: break

print("li $v0, 1")
print("syscall")

print("jr $ra")

f.close()
