import hashlib

def crack(hash):
    brute = ""
    num=100000

    while brute != hash and num < 1000000:
        brute = hashlib.md5(str(num).encode()).hexdigest()
        num+=1
    print(f"FOUND PASSWORD - Correct value for hash {hash} is {num-1}")


hash_input = "3cc6520a6890b92fb55a6b3d657fd1f6"
crack(hash_input)