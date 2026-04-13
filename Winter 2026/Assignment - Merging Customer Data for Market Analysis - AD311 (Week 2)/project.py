# Inputs
customerData1 = [101,104,107,0,0,0]
m = 3
customerData2 = [102,105,108]
n = 3

# Function definition
def mergeCustomerData(customerData1, m, customerData2, n):
    i = m - 1
    j = n - 1
    k = (m + n) - 1
    while j >= 0:
        if customerData1[i] > customerData2[j] and i >= 0:
            customerData1[k] = customerData1[i]
            i -= 1
        else:
            customerData1[k] = customerData2[j]
            j -=1
        k -= 1
    return customerData1

# Function call
result = mergeCustomerData(customerData1, m, customerData2, n)

# Output - [101, 102, 104, 105, 107, 108]
print(result)



