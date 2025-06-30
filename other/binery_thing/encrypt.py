def encrypt_file(path):
    with open(path, "rb") as f:
        data = f.read()

    encrypted = bytes(b ^ 3 for b in data)

    with open(path, "wb") as f:
        f.write(encrypted)
encrypt_file("text.txt")
