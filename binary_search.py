"""
Searching in rotated sorted array. We can use binary search to find the lowest element: the array pivot index. 
With that, we can deduce which portion of the array the element must be in and find it with another binary search on the subarray.

Time: O(log n)
Space: O(1)
"""

def search(array, target):

    def find_lowest(array):
        left = 0
        right = len(array) - 1
        while left < right:
            mid = (left + right) // 2
            # If the middle element is greater than the right element, then the pivot must come after the midpoint.
            if array[mid] > array[right]:
                left = mid + 1
            else:
                right = mid
        return left
    
    def binary_search(array, target, left, right):
        while left <= right:
            mid = (left + right) // 2
            if array[mid] == target:
                return mid
            elif array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    pivot_idx: int = find_lowest(array)
    # cover corner case of null rotation
    if array[pivot_idx] == target:
        return pivot_idx
    elif pivot_idx == 0:
        return binary_search(array, target, 0, len(array) - 1)
    # If the target is less than the first element, it must be right of the pivot.
    elif target < array[0]:
        return binary_search(array, target, pivot_idx, len(array) - 1)
    # Otherwise, it must be left of the pivot
    else:
        return binary_search(array, target, 0, pivot_idx - 1)

    
if __name__ == "__main__":
    A = list(range(0, 10, 2))

    tests = [
        [A, 6, 3],
        [A[3:] + A[:3], 6, 0],
        [[4,5,6,7,0,1,2], 0, 4],
        [[4,5,6,7,0,1,2], 3,-1]
    ]
    
    for test in tests:
        expected = test[2]
        params = test[:2]
        result = search(*params)
        assert result == expected, f"Failed test case with params {params}. Expected {expected} but got {result}" 

    print("All tests passed")
