import win32api as API
import win32gui as UI
import win32 as WIN
import win32con as con
import win32file as WF
# import win32ui as U
import win32com as COM
import winerror
from ctypes import *
from ctypes.wintypes import *
import File as file

import sys


# Globals





# Globals END

'''
Description - Loads the specified bitmap file into memory adn returns a handle to the bitmap.

:param hDC - Handle to the current Device Context.
:param fileName - A string specifying the path to the bitmap file to be loaded.
:returns - A handle to the loaded bitmap.
'''

def loadImgBMP(hDC, fileName):
    if not file.fileExists(fileName):
        raise IOError("File not found")

    err = False
    try:
        hbmp = UI.LoadImage(hDC, fileName, con.IMAGE_BITMAP, 0, 0, con.LR_LOADFROMFILE | con.LR_LOADREALSIZE)
    except Exception:
        err = True

    if not hbmp or err:
        raise IOError("Failed to load bmp")

    return hbmp

'''
Description - Draws a bitmap into the Device Context specified at the given coordinates.

:param hDC - Handle to the Device Context the bitmap will be drawn to.
:param hbmp - A handle to the bitmap
:param x - The x coordinate.
:param y - The y coordinate
:returns True if the function succeeded, otherwise False.
'''

def loadBMPIntoDC(hDC, hbmp, x, y):
    memDC = UI.CreateCompatibleDC(hDC)
    if not memDC:
        return False
    oldHBmp = UI.SelectObject(memDC, hbmp)
    if not oldHBmp:
        UI.DeleteDC(memDC)
        return False

    bm = UI.GetObject(hbmp)
    if con.NULL == UI.BitBlt(hDC, x, y, bm.bmWidth, bm.bmHeight, memDC, 0, 0, con.SRCCOPY):
        UI.DeleteDC(memDC)
        return False

    UI.SelectObject(memDC, oldHBmp)
    UI.DeleteDC(memDC)
    return True

'''
Description - Returns the dimensions of the specified bitmap.
'''

def getBmpDimensions(hbmp):
    bm = UI.GetObject(hbmp)
    ret = [bm.bmWidth, bm.bmHeight]
    return ret

# Draws a circle to the specified DC at (x, y) with diameter of diam.

def drawCircle(hdc, x, y, diam):
    radius = int(diam / 2)
    tlX = x - radius
    tlY = y - radius
    brX = x + radius
    brY = y + radius
    UI.Ellipse(hdc, tlX, tlY, brX, brY)

# Creates an input box at (x, y) with dimensions width and height, with an the id specified which will be used as a notification code in the WndProc.
# hWnd is a handle to the window on which the input box is to be drawn on, an hInstance a handle to the instance of the program.

def createInputBox(x, y, width, height, id, hWnd, hInstance):
    return UI.CreateWindow("EDIT", None, con.WS_CHILD | con.WS_BORDER | con.WS_VISIBLE | con.ES_LEFT | con.ES_MULTILINE,
                           x, y, width, height, hWnd, id, hInstance, None)

# Creates an output box at (x, y) with dimensions width and height, with an the id specified which will be used as a notification code in the WndProc.
# hWnd is a handle to the window on which the input box is to be drawn on, an hInstance a handle to the instance of the program.

def createOutputBox(x, y, width, height, id, hWnd, hInstance):
    hOWnd = createInputBox(x, y, width, height, id, hWnd, hInstance)
    hWWndStyles = UI.GetWindowLong(hOWnd, con.GWL_STYLE)
    UI.SetWindowLong(hOWnd, con.GWL_STYLE, hWWndStyles | con.WS_DISABLED)
    return hOWnd

# Creates a button at (x, y) with dimensions width and height, with an the id specified which will be used as a notification code in the WndProc.
# hWnd is a handle to the window on which the input box is to be drawn on, an hInstance a handle to the instance of the program.

def createButton(text, x, y, width, height, id, hWnd, hInstance):
    return UI.CreateWindow("BUTTON", text,
                           con.WS_CHILD | con.WS_VISIBLE | con.BS_FLAT | con.BS_CENTER | con.BS_PUSHBUTTON, x, y, width,
                           height, hWnd, id, hInstance, None)

# Returns a handle to a font with the specified size, and weight. pPerInch specifies the pixels per inch of the screen.

def createFont(fontSize, pPerInchY, weight, isItalic, isUnderlined, isCrossedOut):
    logFont = UI.LOGFONT()
    logFont.lfHeight = -((fontSize * pPerInchY) / 72)
    logFont.lfWidth = 0
    logFont.lfEscapement = 0
    logFont.lfOrientation = 0
    logFont.lfWeight = weight
    logFont.lfItalic = isItalic
    logFont.lfUnderline = isUnderlined
    logFont.lfStrikeOut = isCrossedOut
    logFont.lfCharSet = con.ANSI_CHARSET
    logFont.lfOutPrecision = con.OUT_DEFAULT_PRECIS
    logFont.lfClipPrecision = con.CLIP_DEFAULT_PRECIS
    logFont.lfQuality = con.DEFAULT_QUALITY
    logFont.lfPitchAndFamily = con.DEFAULT_PITCH | con.FF_DONTCARE
    logFont.lfFaceName = ""

    hFont = UI.CreateFontIndirect(logFont)
    return hFont


# wndclass - Initializes and stores all of the information regarding the WNDCLASS data structure and
# maneges the creation of a window.

class WNDClass:
    def __init__(self, wndProc):  # constructor definition
        self.className = "WNDClass"
        self.hInstance = UI.GetModuleHandle(None)
        self.dwStyle = con.WS_OVERLAPPEDWINDOW

        self.wndClass = UI.WNDCLASS()
        self.wndClass.cbWndExtra = 12
        self.wndClass.style = con.CS_VREDRAW | con.CS_HREDRAW
        self.wndClass.hInstance = self.hInstance
        self.wndClass.lpfnWndProc = wndProc
        self.wndClass.hIcon = UI.LoadIcon(0, con.IDI_APPLICATION)  # Default application icon
        self.wndClass.hCursor = UI.LoadCursor(0, con.IDC_ARROW)  # normal mose pointer as cursor
        self.wndClass.hbrBackground = UI.GetStockObject(con.WHITE_BRUSH)  # white background brush
        self.wndClass.lpszClassName = self.className  # class name doesn't work in python...

        self.wndClassAtom = UI.RegisterClass(self.wndClass)  # ...so the ATOM must be used

    def setResizable(self, isResizable):
        if not isResizable:
            self.dwStyle ^= con.WS_THICKFRAME | con.WS_MAXIMIZEBOX

    def createWindow(self, title):
        self.hwnd = UI.CreateWindow(self.wndClassAtom, title, self.dwStyle, con.CW_USEDEFAULT,
                                    con.CW_USEDEFAULT, con.CW_USEDEFAULT, con.CW_USEDEFAULT, 0, 0, self.hInstance, None)

        # 4 - 7th parameter:
        # horizontal, vertical, x, y default positions and dimensions

        UI.ShowWindow(self.hwnd, con.SW_SHOWNORMAL)  # send the first WM_PAIN msg
        UI.UpdateWindow(self.hwnd)

    def start(self):
        UI.PumpMessages()  # this is actually a loop
