inventory = [4, 0, 1, 3, 0, 2, 5, 0]

def duplicate_zero(inventory):
    n = len(inventory)
    zero = inventory.count(0)

    i = n - 1
    j = (n + zero) - 1

    while i >= 0:
        if j < n:
            inventory[j] = inventory[i]
        if inventory[i] == 0:
            j -= 1
            if j < n:
                inventory[j] = 0
        i -= 1
        j -= 1
    return inventory

result = duplicate_zero(inventory)
print(result)


