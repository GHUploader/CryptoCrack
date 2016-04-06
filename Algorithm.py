
'''
Description - Finds the given element in the specified array. The starting point of the search may be specified,
                but it defaults to 0. The function may find the positions of all elements inside the array that match
                the specified element, or find the position of the first element in the array that matches with the
                specified element.

:param arr - The array to search in.
:param elem - The element to search for
:param start - The starting index of the search. Defaults to 0.
:param fAll - If True, then the positions of all elements in the array that match elem will be found. Otherwise, only
                the position of the first matching element will obtained.

:return positions - An array containing the indexes of the elements from the array that equal to elem.
'''


def find(arr, elem, start=0, fAll=False):
    aSize = arr.__len__()
    positions = []
    for i in range(start, aSize, 1):
        if elem == arr[i]:
            positions.append(i)
            if not fAll:
                break
    return positions


def contains(arr, elem):
    pos = find(arr, elem)
    if pos.__len__() > 0:
        return True
    return False

def digitCount(val):
    return str(val).__len__()


