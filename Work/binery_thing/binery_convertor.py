def binaryConversion(input , size):
    Number=input
    Remainder=0
    output = ""
    more = 0
    while Number != 0:
        Remainder=Number%2
        Number=int(Number/2)
        output += str(Remainder)

    more = size-len(output)
    
    if more >= 0:
        for i in range(1,more):
            output+="0"
        print(output[::-1])
    elif more < 0:
        print(f"Error: The number {input} needs {len(output)} bits, but only {size} were requested.")
        return
    
    

binaryConversion(42,16)