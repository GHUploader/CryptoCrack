
import win32api as API
import win32gui as UI
import win32 as WIN
import win32con as con
from ctypes import *
from ctypes.wintypes import *

import sys


# wndProc gets calles by the OS every single time the windows is repainted. All drawing must be done below WM_PAINT.
# painting has to be done fast so that the window doesn't stop responding, or lag

def wndProc(hwnd, uMsg, wParam, lParam):

    if(uMsg == con.WM_CREATE):
        return 0
    elif uMsg == con.WM_CLOSE:
        UI.DestroyWindow(hwnd)                          # here you could prompt the user if they really want to exit or something
        return 0
    elif uMsg == con.WM_DESTROY:                        # trigerred when DestroyWindow is called
        UI.PostQuitMessage(0)                           # If this is omitted, the program won't close after the window closes
        return 0
    elif uMsg == con.WM_QUIT:                           # triggered when PostQuitMessage is called
        return 0
    elif uMsg == con.WM_SIZE:                           # recompute the sizes of each component to be painted. This event is called when the window is resized
        return 0
    elif uMsg == con.WM_PAINT:
        hDC, paintStruct = UI.BeginPaint(hwnd)          # returns handle to the device context and the paint structure


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


    def start(self):
        UI.PumpMessages()                                     # this is actually a loop
