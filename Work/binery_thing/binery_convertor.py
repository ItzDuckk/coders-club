def twos_complement(val, size):
    # range-check
    if val < 0:
        print("Error: pass a non-negative value (the function negates it).")
        return
    if val >= (2 ** size):
        print(f"Error: {val} needs more than {size} bits.")
        return

    mask = (2 ** size) - 1
    flipped = (~val + 1) & mask

    output = ''

    for i in  range(size-1 , -1 , -1):
        if (flipped >> i) & 1:
            output += '1'
        else:
            output += '0'

    print(output)

twos_complement(42, 8)

