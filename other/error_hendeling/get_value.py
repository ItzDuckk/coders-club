def get_value(dictionary,key):
    try:
        value = dictionary[key]
        print(f"The Key '{key} has a value of '{value}'")
    except KeyError:
        print(f"Error: '{key}' is not a key")