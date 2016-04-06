
import Point as pt
import random
'''


:param rect - Standard win32 RECT structure: (left, top, right, bottom)
:param secCount - Number of sections to split up the field in. This value will equal to the number of points generated,
    and will also determine the density of the points.
:returns - An array containing all of the point objects with valid, random coordinates/
'''

def generateCoords(rect, secCount):
    sectLength = (rect[2] - rect[0]) / secCount
    points = []
    index = 0
    secIndex = rect[0]
    while index < secCount:
        point = pt.Point()
        rXVal = random.randint(secIndex, secIndex + sectLength - 1)
        rYVal = random.randint(rect[1], rect[3])
        point.setX(rXVal)
        point.setY(rYVal)
        points.append(point)
        index += 1
        secIndex += sectLength
    return points

'''
Description - Converts an array of points to an array of strings.

:points - Array of point objects.
:returns - A string made up of the X and Y coordinate pairs contained by the different point objects in the array.
'''

def pointsToStr(points):
    index = 0
    size = points.__len__()
    ret = []
    while index < size:
        tmp = points[index].toString()
        ret.append(tmp)
        index += 1
    return ret

def strArrToString(strArr):
    retStr = ""
    for i in range(0, strArr.__len__(), 1):
        retStr += strArr[i].__str__()
    return retStr

'''
Purpose - Checks if the given string contains the valid characters specified by the given range.

:param str - The string to validate
:param startAscii - The value specifying the lower bound of the valid character range.
:param endAscii - The value specifying the upper bound of the valid character range.

Return Value:
    Returns False if the string contains a value outside of the specified range, otherwise returns True.

Note: The values specifying the valid range of characters are ASCII values

'''

def validateStr(str, startAscii, endAscii):
    index = 0
    size = str.__len__()
    while index < size:
        char = str[index]
        iChar = ord(char)
        if not startAscii <= iChar <= endAscii:
            return False
        index += 1
    return True


'''
Description - Takes in a string and adds the specified offset to every character in the string.

:param word - A string containing the characters to be encrypted. An array is also acceptable.
:param offset - The value to be added to every single character.

:returns - Array of the encrypted character codes.
'''

def encryptStr(word, offset):
    index = 0
    size = word.__len__()
    encrypted = []

    while index < size:
        char = word[index]
        charCode = ord(char)
        encCharCode = charCode + offset
        encrypted.append(str(encCharCode))
        index += 1

    return encrypted

'''
Description - Encrypts the given string.

:param word - string to encrypt
:returns - encrypted string
'''

def encryptWord(word):
    offset = random.randint(1, 20)
    return encryptStr(word, offset)

'''
Description - Encrypts the specified array of words, and adds spaces between the words in the array if it is specified.

:strArr - Array of strings.
:space - Defaults to False. Read the next parameter description for details.
:returns - A string containing the encrypted words from the array. Spaces are added if space = True
'''

def encryptWords(strArr, space=False):
    ret = []
    offset = random.randint(1, 20)
    for i in range(0, strArr.__len__(), 1):
        ret += encryptStr(strArr[i], offset)
        if space:
            ret.append('  ')
    return ret
