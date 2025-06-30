import sys, re

def pretty_print(words):

    for key in words:
        value = words[key]
        print(f"The word \"{key}\" appear {value} times")

def get_top(words,N):
    top = {}
    
    if N > len(words):
        N = len(words)

    for i in range(1,N+1):
        max_count = max(words,key=words.get)
        top[max_count] = words[max_count]
        del words[max_count]
    return top

def count_words(string):
    words = string.split()

    appearance_of_each_word = {}
    for word in words:
        if word in appearance_of_each_word:
            appearance_of_each_word[word] += 1
        else:
            appearance_of_each_word[word] = 1
    
    return appearance_of_each_word


def read_file(location):
    try:
        with open(location, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file '{location}' was not found.")

def main():
    file_location = sys.argv[1]
    amount = sys.argv[2]

    try:
        amount_int = int(amount)
        if amount_int <= 0:
            print("Error: amount must be bigger then 0")
            exit()
    except ValueError:
        print(f"Error: '{amount}' isn’t a valid integer.")
        exit()
    
    string = read_file(file_location)
    count = count_words(string)
    top = get_top(count,amount_int)
    pretty_print(top)

if __name__ == "__main__":
    main()