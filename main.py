
import Windows as win
import File as f
import string
import win32con as con
import win32gui as UI
import win32api as api
import win32com as com
import win32ui as WUI




# ########################
# Globals

hBmp = 0
windowCreated = False
hWndInputX = 0
hWndInputY = 0
hWndCoordBtn = 0
hFont = 0

xCoord = 100
yCoord = 100

ID_XCINPUT = 100
ID_YCINPUT = 101
ID_COORDBTN = 200

# Globals END
# ########################



# wndProc gets calles by the OS every single time the windows is repainted. All drawing must be done below WM_PAINT.
# painting has to be done fast so that the window doesn't stop responding, or lag

def wndProc(hwnd, uMsg, wParam, lParam):
    global hBmp
    global windowCreated
    global hWndInputX
    global hWndInputY
    global hWndCoordBtn
    global hFont

    if uMsg == con.WM_CREATE:                   # Python buf: WM_CREATE never gets called, use sendmessage
        hInstance = UI.GetWindowLong(hwnd, con.GWL_HINSTANCE)
        hWndInputX = win.createInputBox(0, 500, 100, 20, ID_XCINPUT, hwnd, hInstance)
        hWndInputY = win.createInputBox(120, 500, 100, 20, ID_YCINPUT, hwnd, hInstance)
        hWndCoordBtn = win.createButton("Move", 240, 500, 100, 22, ID_COORDBTN, hwnd, hInstance)
        UI.SendMessage(hWndCoordBtn, con.WM_SETFONT, hFont, True)
        UI.SendMessage(hWndInputX, con.WM_SETFONT, hFont, True)
        UI.SendMessage(hWndInputY, con.WM_SETFONT, hFont, True)
        UI.SetWindowPos(hwnd, 0, 0, 0, 1000, 575, con.SWP_NOMOVE | con.SWP_NOZORDER)
        return 0
    elif uMsg == con.WM_CLOSE:
        UI.DestroyWindow(hwnd)
        return 0
    elif uMsg == con.WM_DESTROY:                        # trigerred when DestroyWindow is called
        UI.DestroyWindow(hWndInputX)
        UI.DestroyWindow(hWndInputY)
        UI.DestroyWindow(hWndCoordBtn)
        UI.DeleteObject(hFont)
        UI.DeleteObject(hBmp)
        UI.PostQuitMessage(0)
        return 0
    elif uMsg == con.WM_QUIT:                           # triggered when PostQuitMessage is called, but it's not called as it's supposed to...
        #closeHandles()
        return 0
    elif uMsg == con.WM_SIZE:                           # recompute the sizes of each component to be painted. This event is called when the window is resized

        return 0
    elif uMsg == con.WM_PAINT:
        hDC, paintStruct = UI.BeginPaint(hwnd)  # returns handle to the device context and the paint structure

        if not windowCreated:
            hBmp = win.loadImgBMP(hDC, "grass.bmp")
            hFont = win.createFont(10, WUI.GetDeviceCaps(hDC, con.LOGPIXELSY), con.FW_NORMAL, False, False, False)

        if not win.loadBMPIntoDC(hDC, hBmp, 0, 0):
            UI.PostQuitMessage(0)
            raise SystemError("Failed to load bmp")

        oldHPB = UI.SelectObject(hDC, UI.GetStockObject(con.BLACK_BRUSH))

        win.drawCircle(hDC, xCoord, yCoord, 20)

        UI.SelectObject(hDC, oldHPB)

        UI.EndPaint(hwnd, paintStruct)                  # resources must be released when painting is done

        if not windowCreated:
            UI.SendMessage(hwnd, con.WM_CREATE, 0, 0)
            windowCreated = True

        return 0
    elif uMsg == con.WM_COMMAND:

        return 0
    else:
        return UI.DefWindowProc(hwnd, uMsg, wParam, lParam)     # if msg handler is not defined, then do nothing

# end of function



def main():
    file = f.File("test.txt", True, False)
    fData = file.getFileData()
    print(fData)
    print(fData[0])             # 82 is the ascii code for R

    window = win.WNDClass(wndProc)
    window.setResizable(False)
    window.createWindow("Crypto-Crack")
    window.start()

main()




