def insertionsort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >=0 and key < arr[j] :
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def main():
    arr = [12, 11, 13, 5, 6]
    arr2 = [38, 27, 43, 3, 9, 82, 10]
    sorted_arr = insertionsort(arr)
    sorted_arr2 = merge_sort(arr2)
    print("Sorted array is:", sorted_arr)
    print("Sorted array is:", sorted_arr2)

if __name__ == "__main__":
    main()