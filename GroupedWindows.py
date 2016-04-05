
import win32gui as UI
import win32ui as U
import win32con as con
import Windows as win

class GroupedWindows:

    def __init__(self, parentHWnd, x = con.CW_USEDEFAULT, y = con.CW_USEDEFAULT, width = con.CW_USEDEFAULT, height = con.CW_USEDEFAULT):
        self.hInstance = UI.GetWindowLong(parentHWnd, con.GWL_HINSTANCE)
        self.hGWnd = UI.CreateWindow("BUTTON", "", con.WS_CHILD | con.WS_VISIBLE | con.BS_GROUPBOX, x, y, width, height, parentHWnd, 0, self.hInstance, None)

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
        UI.DestroyWindow(self.hGWnd)

    def setFont(self, hFont):
        UI.SendMessage(self.hGWnd, con.WM_SETFONT, hFont, True)