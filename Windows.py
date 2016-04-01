
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
global hBmp
global windowCreated
global hWnd             # win32 complications...


hBmp = 0
windowCreated = False
hWnd = 0

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



# wndProc gets calles by the OS every single time the windows is repainted. All drawing must be done below WM_PAINT.
# painting has to be done fast so that the window doesn't stop responding, or lag

def wndProc(hwnd, uMsg, wParam, lParam):
    global hBmp
    global windowCreated
    global hWnd

    if uMsg == con.WM_CREATE:                   # Python buf: WM_CREATE never gets called, use sendmessage
        #hWnd = hwnd
        hDC, paintStruct = UI.BeginPaint(hwnd)

        UI.EndPaint(hwnd, paintStruct)
        return 0
    elif uMsg == con.WM_CLOSE:
        UI.DestroyWindow(hwnd)                          # here you could prompt the user if they really want to exit or something
        return 0
    elif uMsg == con.WM_DESTROY:                        # trigerred when DestroyWindow is called
        UI.PostQuitMessage(0)                           # If this is omitted, the program won't close after the window closes

        return 0
    elif uMsg == con.WM_QUIT:                           # triggered when PostQuitMessage is called, but it's not called as it's supposed to...
        #closeHandles()
        return 0
    elif uMsg == con.WM_SIZE:                           # recompute the sizes of each component to be painted. This event is called when the window is resized
        return 0
    elif uMsg == con.WM_PAINT:
        hDC, paintStruct = UI.BeginPaint(hwnd)  # returns handle to the device context and the paint structure

        if not windowCreated:
            hBmp = loadImgBMP(hDC, "grass.bmp")
            windowCreated = True


        if not loadBMPIntoDC(hDC, hBmp, 0, 0):
            UI.PostQuitMessage(0)
            raise SystemError("Failed to load bmp")

        UI.MoveToEx(hDC, 10, 10)
        UI.LineTo(hDC, 100, 100)

        UI.EndPaint(hwnd, paintStruct)                  # resources must be released when painting is done
        return 0
    else:
        return UI.DefWindowProc(hwnd, uMsg, wParam, lParam)     # if msg handler is not defined, then do nothing

# end of function

# wndclass - Initializes and stores all of the information regarding the WNDCLASS data structure and
# maneges the creation of a window.

class WNDClass:

    def __init__(self):                                                         # constructor definition
        self.className = "WNDClass"
        self.hInstance = UI.GetModuleHandle(None)                               # get handle to the current instance of the program from the OS

        self.wndClass = UI.WNDCLASS()                                           # call constructor ( does nothing in this case )
        self.wndClass.style = con.CS_VREDRAW | con.CS_HREDRAW                   # styles...
        self.wndClass.lpfnWndProc = wndProc                                     # set the wnd procedure
        self.wndClass.hInstance = self.hInstance                                # handle to the current instance
        self.wndClass.hIcon = UI.LoadIcon(0, con.IDI_APPLICATION)               # Default application icon
        self.wndClass.hCursor = UI.LoadCursor(0, con.IDC_ARROW)                 # normal mose pointer as cursor
        self.wndClass.hbrBackground = UI.GetStockObject(con.WHITE_BRUSH)        # white background brush
        self.wndClass.lpszClassName = self.className

        self.wndClassAtom = UI.RegisterClass(self.wndClass)                     # register class.




    def createWindow(self, title):
        self.hwnd = UI.CreateWindow(self.wndClassAtom, title, con.WS_OVERLAPPEDWINDOW, con.CW_USEDEFAULT,
                                    con.CW_USEDEFAULT, con.CW_USEDEFAULT, con.CW_USEDEFAULT, 0, 0, self.hInstance, None)

        # 4 - 7th parameter:
        # horizontal, vertical, x, y default positions and dimensions

        UI.ShowWindow(self.hwnd, con.SW_SHOWNORMAL)           # send the first WM_PAIN msg
        UI.UpdateWindow(self.hwnd)

        # global hWnd
        # self.hwnd = hWnd



    def start(self):
        UI.PumpMessages()                                     # this is actually a loop
