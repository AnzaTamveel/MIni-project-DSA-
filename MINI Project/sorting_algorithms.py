import pandas as pd

def insertion_sort(series, column_index):
    # Create a copy of the Series to avoid modifying the original
    sorted_series = series.copy()

    # Insertion sort algorithm
    for i in range(1, len(sorted_series)):
        key = sorted_series[i]
        j = i - 1

        while j >= 0 and sorted_series[j] > key:
            sorted_series[j + 1] = sorted_series[j]
            j -= 1

        sorted_series[j + 1] = key

    return sorted_series

def merge_sort(series):
    # Create a copy of the Series to avoid modifying the original
    sorted_series = series.copy()
    
    if len(sorted_series) <= 1:
        return sorted_series

    mid = len(sorted_series) // 2
    left_half = merge_sort(sorted_series[:mid])
    right_half = merge_sort(sorted_series[mid:])

    return merge(left_half, right_half)

def merge(left, right):
    sorted_series = []
    left_index = right_index = 0

    # Compare elements from both halves and build the sorted series
    while left_index < len(left) and right_index < len(right):
        if left.iloc[left_index] <= right.iloc[right_index]:
            sorted_series.append(left.iloc[left_index])
            left_index += 1
        else:
            sorted_series.append(right.iloc[right_index])
            right_index += 1

    # Append remaining elements from left half, if any
    if left_index < len(left):
        sorted_series.extend(left.iloc[left_index:])
    # Append remaining elements from right half, if any
    if right_index < len(right):
        sorted_series.extend(right.iloc[right_index:]) 

    return pd.Series(sorted_series)  # Return as a Series


def bubble_sort(series):
    sorted_series = series.copy()
    n = len(sorted_series)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if custom_sort_key(sorted_series[j]) > custom_sort_key(sorted_series[j + 1]):
                sorted_series[j], sorted_series[j + 1] = sorted_series[j + 1], sorted_series[j]

    return sorted_series

def custom_sort_key(value):
    try:
        return float(value)  # Attempt to convert to float for numeric comparison
    except (ValueError, TypeError):
        return value  # Fallback to original value for strings


def selection_sort(series):
    sorted_series = series.copy()
    n = len(sorted_series)

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if custom_sort_key(sorted_series[j]) < custom_sort_key(sorted_series[min_index]):
                min_index = j
        sorted_series[i], sorted_series[min_index] = sorted_series[min_index], sorted_series[i]

    return sorted_series

def counting_sort(series):
    # Filter numeric values and count their occurrences
    numeric_series = series.apply(pd.to_numeric, errors='coerce').dropna()
    if numeric_series.empty:
        return series  # Return original series if no numeric values
    
    max_value = int(numeric_series.max())
    min_value = int(numeric_series.min())
    range_of_elements = max_value - min_value + 1
    
    count = [0] * range_of_elements
    sorted_series = [0] * len(series)
    
    # Count occurrences of each numeric element
    for num in numeric_series:
        count[int(num) - min_value] += 1
    
    # Change count[i] so that it contains the actual position of this number in sorted array
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Build the output sorted array
    for i in range(len(series) - 1, -1, -1):
        if pd.to_numeric(series[i], errors='coerce') is not None:
            sorted_series[count[int(series[i]) - min_value] - 1] = series[i]
            count[int(series[i]) - min_value] -= 1
        else:
            sorted_series[i] = series[i]  # Keep non-numeric values in their position

    return pd.Series(sorted_series)

def radix_sort(series):
    numeric_series = series.apply(pd.to_numeric, errors='coerce').dropna()
    if numeric_series.empty:
        return series

    numeric_series = numeric_series.astype(int)
    max_value = numeric_series.max()

    exp = 1
    while max_value // exp > 0:
        numeric_series = counting_sort_radix(numeric_series, exp)
        exp *= 10
    
    return numeric_series

def counting_sort_radix(series, exp):
    n = len(series)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = (series.iloc[i] // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (series.iloc[i] // exp) % 10
        output[count[index] - 1] = series.iloc[i]
        count[index] -= 1

    for i in range(n):
        series.iloc[i] = output[i]

    return series

def bucket_sort(data):
    data = pd.to_numeric(data, errors='coerce')
    data = data.dropna()

    if len(data) == 0:
        return data

    # Create buckets
    min_value = data.min()
    max_value = data.max()
    bucket_count = 10  # You can adjust this based on your needs
    bucket_size = (max_value - min_value) / bucket_count
    buckets = [[] for _ in range(bucket_count)]

    # Place data into buckets
    for value in data:
        index = int((value - min_value) / bucket_size)
        if index == bucket_count:  # Handle the edge case for the maximum value
            index -= 1
        buckets[index].append(value)
    sorted_series = pd.Series(dtype=data.dtype)
    for bucket in buckets:
        sorted_series = pd.concat([sorted_series, pd.Series(sorted(bucket))], ignore_index=True)

    return sorted_series

# Shell Sort
def shell_sort(series):
    copy_series = series.copy()
    n = len(copy_series)
    gap = n // 2
    while gap > 0:
        for i in range(gap , n):
            t = copy_series[i]
            j = i
            while j >= gap and custom_sort_key(copy_series[j - gap]) > custom_sort_key(t):
                copy_series[j] = copy_series[j - gap]
                j -= gap
            copy_series[j] = t
        gap //= 2
    return copy_series

# Heap Sort
def heap_sort(series):
    sorted_series = series.copy()
    n = len(sorted_series)

    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        # Compare left child
        if l < n and custom_sort_key(arr[l]) > custom_sort_key(arr[largest]):
            largest = l
        # Compare right child
        if r < n and custom_sort_key(arr[r]) > custom_sort_key(arr[largest]):
            largest = r
        # If largest is not the root
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
            heapify(arr, n, largest)  # Recursively heapify the affected sub-tree

    # Build a maxheap
    for i in range(n // 2 - 1, -1, -1):
        heapify(sorted_series, n, i)

    # One by one extract elements from heap
    for i in range(n - 1, 0, -1):
        sorted_series[i], sorted_series[0] = sorted_series[0], sorted_series[i]  # Swap
        heapify(sorted_series, i, 0)  # Heapify the root element

    return sorted_series


# Quick Sort
def quick_sort(series):
    if len(series) <= 1:
        return series

    # Reset index to ensure numerical indices
    series = series.reset_index(drop=True)

    # Choose the pivot
    pivot = series[len(series) // 2]

    # Partition the data
    left = series[series.apply(custom_sort_key) < custom_sort_key(pivot)]
    middle = series[series.apply(custom_sort_key) == custom_sort_key(pivot)]
    right = series[series.apply(custom_sort_key) > custom_sort_key(pivot)]

    # Recursively sort and concatenate the results
    return pd.concat([quick_sort(left), middle, quick_sort(right)])

# Comb Sort
def comb_sort(series):
    sorted_series = series.copy()
    n = len(sorted_series)
    gap = n
    shrink = 1.3  # Shrinking factor
    sorted = False

    while not sorted:
        # Update the gap for the next comparison
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        
        for i in range(n - gap):
            if custom_sort_key(sorted_series[i]) > custom_sort_key(sorted_series[i + gap]):
                sorted_series[i], sorted_series[i + gap] = sorted_series[i + gap], sorted_series[i]
                sorted = False
    
    return sorted_series