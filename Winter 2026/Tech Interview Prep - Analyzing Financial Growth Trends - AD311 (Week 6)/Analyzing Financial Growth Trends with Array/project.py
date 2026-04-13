def growth_squares(growthPercentages):
    n = len(growthPercentages)
    position = n - 1
    left = 0
    right = n - 1
    result = [0] * n

    while left <= right:
        if abs(growthPercentages[left]) > abs(growthPercentages[right]):
            result[position] = growthPercentages[left] ** 2
            left += 1
        else:
            result[position] = growthPercentages[right] ** 2
            right -= 1
        position -= 1
    return result




print(growth_squares([-5, -2, 0, 3, 10]))