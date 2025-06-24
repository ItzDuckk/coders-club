def count_values_in_tuples(tuples_list):
    counts = {}
    for slot in tuples_list:
        for val in slot:
            if val in counts:
                counts[val] += 1
            else:
                counts[val] = 1
    return counts

tuples = [('a', 'b'), ('a', 'c'), ('d', 'b'), ('e', 'f'), ('a', 'b')]
result = count_values_in_tuples(tuples)
print(result)
