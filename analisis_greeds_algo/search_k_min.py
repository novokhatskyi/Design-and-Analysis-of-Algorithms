def search_k_min(arr, k):
    if not arr:
        raise ValueError("Масив не може бути порожнім")

    if k < 1 or k > len(arr):
        raise ValueError("k має бути від 1 до довжини масиву")

    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    if k <= len(left):
        return search_k_min(left, k)

    elif k <= len(left) + len(middle):
        return pivot

    else:
        return search_k_min(right, k - len(left) - len(middle))


arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
k = 3

result = search_k_min(arr, k)
print(f"The {k}-th minimum element is: {result}")