
import win32gui as UI
#import win32ui as U
import win32api as API
import win32con as con
import Windows as win
import ctypes

import Algorithm as a

def findObjByHWND(hwnd):
    for i in range(0, GroupedWindows.inst.__len__(), 1):
        if GroupedWindows.inst[i].hGWnd == hwnd:
            return GroupedWindows.inst[i]
    return None

def wndProc(hwnd, uMsg, wParam, lParam):

    gwObj = findObjByHWND(hwnd)
    return gwObj.wndProc(hwnd, uMsg, wParam, lParam)


class GroupedWindows:

    inst = []

    def __init__(self, parentHWnd, x = con.CW_USEDEFAULT, y = con.CW_USEDEFAULT, width = con.CW_USEDEFAULT, height = con.CW_USEDEFAULT):
        self.hInstance = UI.GetWindowLong(parentHWnd, con.GWL_HINSTANCE)
        self.hGWnd = UI.CreateWindow("BUTTON", "", con.WS_CHILD | con.WS_VISIBLE | con.BS_GROUPBOX, x, y, width, height, parentHWnd, 0, self.hInstance, None)
        self.onCommand = None
        self.iWndProc = None
        self.exit = False
        GroupedWindows.inst.append(self)

    def __del__(self):
        GroupedWindows.inst.remove(self)

    def setBrush(self, color):
        hdc = UI.GetDC(self.hGWnd)
        UI.SetBkColor(hdc, color)
        UI.ReleaseDC(self.hGWnd, hdc)

    def setTitleText(self, text):
        UI.SetWindowText(self.hGWnd, text)

    def addChild(self, hwnd, x = 0, y = 0):
        UI.SetParent(hwnd, self.hGWnd)
        UI.SetWindowPos(hwnd, 0, x, y, 0, 0, con.SWP_NOZORDER | con.SWP_NOSIZE)

    def destroyWindow(self):
        if self.onCommand != None:

            funcType = ctypes.CFUNCTYPE(ctypes.c_longlong, win.HANDLE, win.UINT, win.WPARAM, win.LPARAM)
            cIWndProc = funcType(self.iWndProc)
            UI.SetWindowLong(self.hGWnd, con.GWL_WNDPROC, cIWndProc)
            UI.SetWindowPos(self.hGWnd, 0, 0, 0, 0, 0, con.SWP_NOSIZE | con.SWP_NOMOVE | con.SWP_NOZORDER)

            #self.exit = True
        UI.CloseWindow(self.hGWnd)

    def setFont(self, hFont):
        UI.SendMessage(self.hGWnd, con.WM_SETFONT, hFont, True)

    def setCommandHandler(self, handler):
        self.onCommand = handler
        self.iWndProc = API.GetWindowLong(self.hGWnd, con.GWL_WNDPROC)
        UI.SetWindowLong(self.hGWnd, con.GWL_WNDPROC, wndProc)

    def wndProc(self, hwnd, uMsg, wParam, lParam):
        if uMsg == con.WM_COMMAND and not self.exit:
            return self.onCommand(hwnd, uMsg, wParam, lParam)
        if not self.exit:
            return UI.CallWindowProc(self.iWndProc, hwnd, uMsg, wParam, lParam)
        return UI.DefWindowProc(hwnd, uMsg, wParam, lParam)