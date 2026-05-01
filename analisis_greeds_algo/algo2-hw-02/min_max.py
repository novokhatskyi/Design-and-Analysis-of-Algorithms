from rich import print

def search_min_max(arr, left, right):
    if left == right:
        return (arr[left], arr[left])
    elif right == left + 1:
        if arr[left] < arr[right]:
            return (arr[left], arr[right])
        else:
            return (arr[right], arr[left])
    else:
        mid = (left + right) // 2
        left_min_max = search_min_max(arr, left, mid)
        right_min_max = search_min_max(arr, mid + 1, right)
        min_value = min(left_min_max[0], right_min_max[0])
        max_value = max(left_min_max[1], right_min_max[1])
        return (min_value, max_value)


# Example usage
if __name__ == "__main__":
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    min_max = search_min_max(arr, 0, len(arr) - 1)
    print(f"Minimum and Maximum elements: {min_max}")

    