def reverse_string(s):
    if s == "":
        return ""
    return reverse_string(s[1:]) + s[0]


result = reverse_string("abc")
print(result)