def get_input():
    positive_decimal = int(input("Enter a positive integer:"))
    byte_size = int(input("Enter the memory size in bits:"))
    try:   
        input > 0
    except:
        print("Error: input must be Positive")
    
    return positive_decimal,byte_size

def decimal_to_binary(decimal,bits):
    return str(bin(decimal))[2::1].zfill(bits)

def twos_complement(decimal,bits):
   inverted_binary = ''.join('1' if bit == '0' else '0' for bit in decimal)
   decimal_inverted = int(inverted_binary,base=2) + 1
   return decimal_to_binary(decimal_inverted,bits)

def main():
    decimal,memory = get_input()
    binary = decimal_to_binary(decimal,memory)
    inverted = twos_complement(binary,memory)
    print(inverted)

if __name__ == "__main__":
    main()