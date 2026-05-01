def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot =  arr[len(arr) // 2]
    left = [el for el in arr if el < pivot]
    middle = [el for el in arr if el == pivot]
    right = [el for el in arr if el > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Example usage
if __name__ == "__main__":
    print("Enter the number of elements in the array:")
    n = int(input())
    arr = []
    print("Enter the elements of the array:")
    for _ in range(n):
        arr.append(int(input()))
    sorted_arr = quick_sort(arr)
    print("Sorted array:", sorted_arr)
    print("Minimum element:", sorted_arr[0])
    print("Maximum element:", sorted_arr[-1])