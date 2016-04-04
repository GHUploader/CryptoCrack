
import Point as pt
import random
'''


param rect - Standard win32 RECT structure: (left, top, right, bottom)
param secCount - Number of sections to split up the field in. This value will equal to the number of points generated,
    and will also determine the density of the points.
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

param str - The string to validate
param startAscii - The value specifying the lower bound of the valid character range.
param endAscii - The value specifying the upper bound of the valid character range.

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

def encryptWord(word):
    offset = random.randint(1, 20)
    return encryptStr(word, offset)

def encryptWords(strArr):
    ret = []
    offset = random.randint(1, 20)
    for i in range(0, strArr.__len__(), 1):
        ret += encryptStr(strArr[i], offset)
    return ret
