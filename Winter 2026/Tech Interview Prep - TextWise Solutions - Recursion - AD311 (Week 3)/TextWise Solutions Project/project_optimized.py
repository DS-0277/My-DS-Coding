def reverse_string_optimized(s, index = 0):
    if index == len(s):
        return ""
    return reverse_string_optimized(s, index + 1) + s[index]


result2 = reverse_string_optimized("abc")
print(result2)