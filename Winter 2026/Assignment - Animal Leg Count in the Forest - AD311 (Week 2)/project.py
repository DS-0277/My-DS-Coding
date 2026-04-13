# Inputs
animals_1 = ['lion', 'monkey', 'deer', 'snake', 'elephant']
animals_2 = ['frog', 'horse', 'spider', 'ant']

# Function definition
def count_four_animals(animals):
    four_legged_animals = ['lion', 'deer', 'elephant', 'horse', 'dog', 'cat']
    count = 0
    for animal in animals:
        if animal in four_legged_animals:
            count += 1
    return count

# Function call
result1 = count_four_animals(animals_1)
result2 = count_four_animals(animals_2)

# Output
print(result1)
print(result2)