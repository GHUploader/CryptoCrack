
import win32api as API
import win32gui as UI
import win32 as WIN
import win32con as con
import win32file as WF
import winerror
from ctypes import *
from ctypes.wintypes import *
import File as file

import sys

# Globals





# Globals END

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

def loadBMPIntoDC(hDC, hbmp, x, y):

    memDC = UI.CreateCompatibleDC(hDC)
    if not memDC:
        return False

    if not UI.SelectObject(memDC, hbmp):
        UI.DeleteDC(memDC)
        return False

    bm = UI.GetObject(hbmp)
    if con.NULL == UI.BitBlt(hDC, x, y, bm.bmWidth, bm.bmHeight, memDC, 0, 0, con.SRCCOPY):
        UI.DeleteDC(memDC)
        return False

    UI.DeleteDC(memDC)
    return True

def createInputBox(x, y, width, height, id, hWnd, hInstance):
    return UI.CreateWindow("EDIT", None, con.WS_CHILD | con.WS_BORDER | con.WS_VISIBLE | con.ES_LEFT | con.ES_MULTILINE, x, y, width, height, hWnd, id, hInstance, None)

def createButton(text, x, y, width, height, id, hWnd, hInstance):
    return UI.CreateWindow("BUTTON", text, con.WS_CHILD | con.WS_VISIBLE | con.BS_FLAT | con.BS_CENTER | con.BS_PUSHBUTTON, x, y, width, height, hWnd, id, hInstance, None)

def createFont(fontSize, pPerInch, weight, isItalic, isUnderlined, isCrossedOut):
    logFont = UI.LOGFONT()
    logFont.lfHeight = -((fontSize * pPerInch) / 72)
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

    def __init__(self, wndProc):                                                         # constructor definition
        self.className = "WNDClass"
        self.hInstance = UI.GetModuleHandle(None)                               # get handle to the current instance of the program from the OS
        self.dwStyle = con.WS_OVERLAPPEDWINDOW

        self.wndClass = UI.WNDCLASS()                                           # call constructor ( does nothing in this case )
        self.wndClass.style = con.CS_VREDRAW | con.CS_HREDRAW                   # styles...
        self.wndClass.lpfnWndProc = wndProc                                     # set the wnd procedure
        self.wndClass.hInstance = self.hInstance                                # handle to the current instance
        self.wndClass.hIcon = UI.LoadIcon(0, con.IDI_APPLICATION)               # Default application icon
        self.wndClass.hCursor = UI.LoadCursor(0, con.IDC_ARROW)                 # normal mose pointer as cursor
        self.wndClass.hbrBackground = UI.GetStockObject(con.WHITE_BRUSH)        # white background brush
        self.wndClass.lpszClassName = self.className

        self.wndClassAtom = UI.RegisterClass(self.wndClass)                     # register class.


    def setResizable(self, isResizable):
        if not isResizable:
            self.dwStyle ^= con.WS_THICKFRAME
            self.dwStyle ^= con.WS_MAXIMIZEBOX

    def createWindow(self, title):
        self.hwnd = UI.CreateWindow(self.wndClassAtom, title, self.dwStyle, con.CW_USEDEFAULT,
                                    con.CW_USEDEFAULT, con.CW_USEDEFAULT, con.CW_USEDEFAULT, 0, 0, self.hInstance, None)

        # 4 - 7th parameter:
        # horizontal, vertical, x, y default positions and dimensions

        UI.ShowWindow(self.hwnd, con.SW_SHOWNORMAL)           # send the first WM_PAIN msg
        UI.UpdateWindow(self.hwnd)

        # global hWnd
        # self.hwnd = hWnd



    def start(self):
        UI.PumpMessages()                                     # this is actually a loop
