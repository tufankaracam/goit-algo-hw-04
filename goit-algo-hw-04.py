import timeit
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def generateList(count):
    return [random.randint(0, 999999) for x in range(count)]


def insertion_sort(lst):
    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        while j >= 0 and key < lst[j]:
            lst[j+1] = lst[j]
            j -= 1
        lst[j+1] = key
    return lst


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    return merge(merge_sort(left_half), merge_sort(right_half))


def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0

    # Спочатку об'єднайте менші елементи
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    # Якщо в лівій або правій половині залишилися елементи,
        # додайте їх до результату
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1

    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged


setup_code = """
from __main__ import generateList, insertion_sort, merge_sort
test_list = generateList({})
"""


counts = [100, 1000, 10000, 25000, 50000]
insert_performance = []
merge_performance = []
sorted_performance = []

for count in counts:
    setup_code_formatted = setup_code.format(count)
    insert_performance.append(timeit.timeit(
        stmt='insertion_sort(test_list[:])', setup=setup_code_formatted, number=1))
    merge_performance.append(timeit.timeit(
        stmt='merge_sort(test_list[:])', setup=setup_code_formatted, number=1))
    sorted_performance.append(timeit.timeit(
        stmt='sorted(test_list)', setup=setup_code_formatted, number=1))


insert_performance = np.array(insert_performance)
merge_performance = np.array(merge_performance)
sorted_performance = np.array(sorted_performance)


data = np.column_stack(
    (insert_performance, merge_performance, sorted_performance))

df = pd.DataFrame(data=data, columns=[
                  'insert', 'merge', 'timsort'], index=counts)


print(df)
df.plot(logy=True)
plt.show()
