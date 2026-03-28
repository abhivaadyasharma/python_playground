def is_monotonic(arr):
    increasing = decreasing = True

    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            increasing = False
        if arr[i] > arr[i - 1]:
            decreasing = False

    return increasing or decreasing


# Input from user
arr = list(map(int, input("Enter array elements separated by space: ").split()))

# Check monotonicity
if is_monotonic(arr):
    print("✅ The array is monotonic.")
else:
    print("❌ The array is not monotonic.")
