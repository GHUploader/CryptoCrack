
import Windows as win
import File as f
import Crypto as cpt
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
hWndCryptoOutput = 0
hFont = 0

xCoord = 0
yCoord = 0

START_XCOORD = 0
START_YCOORD = 0
BMP_XCOORD = 0
BMP_YCOORD = 0

ID_XCINPUT = 100
ID_YCINPUT = 101
ID_COORDBTN = 200

STATUS_OK = 0
STATUS_INVALIDINPUT = 1
STATUS_INPUT_OUTOF_RANGE = 2

ASCII_DEC_START = 48
ASCII_DEC_END = 57

coords = []
encrypted = []
encryptedMsg = ""

# Globals END
# ########################


# ########################################
# WndProc Handler Sub-Procedures

def validateBtnInput(xInput, yInput, rect):
    if xInput and yInput:
        if cpt.validateStr(xInput, ASCII_DEC_START, ASCII_DEC_END) and cpt.validateStr(yInput, ASCII_DEC_START, ASCII_DEC_END):
            xInputI = int(xInput)
            yInputI = int(yInput)
            if BMP_XCOORD <= xInputI <= rect[0] and BMP_YCOORD <= yInputI <= rect[1]:
                return STATUS_OK
            return STATUS_INPUT_OUTOF_RANGE
    return STATUS_INVALIDINPUT

def setFirstCoordinate(points):
    global xCoord
    global yCoord
    point = points[0]
    xCoord = point.getX()
    yCoord = point.getY()
    UI.SetWindowText(hWndInputX, str(xCoord))
    UI.SetWindowText(hWndInputY, str(yCoord))

# ########################################
# ########################################

# ##################################################################
# Internal WndProc Msg Handlers

def initGDI(hwnd):
    global hBmp
    global hFont
    hDC = UI.GetDC(hwnd)
    hBmp = win.loadImgBMP(hDC, "grass.bmp")
    hFont = win.createFont(10, WUI.GetDeviceCaps(hDC, con.LOGPIXELSY), con.FW_NORMAL, False, False, False)
    UI.ReleaseDC(hwnd, hDC)

def createWindowComponents(hwnd):
    global hWndInputX
    global hWndInputY
    global hWndCoordBtn
    global hWndCryptoOutput
    hInstance = UI.GetWindowLong(hwnd, con.GWL_HINSTANCE)
    hWndInputX = win.createInputBox(0, 500, 100, 20, ID_XCINPUT, hwnd, hInstance)
    hWndInputY = win.createInputBox(120, 500, 100, 20, ID_YCINPUT, hwnd, hInstance)
    hWndCoordBtn = win.createButton("Move", 240, 500, 100, 22, ID_COORDBTN, hwnd, hInstance)
    hWndCryptoOutput = win.createOutputBox(650, 10, 325, 515, 0, hwnd, hInstance)

def initWindow(hwnd):
    initGDI(hwnd)
    createWindowComponents(hwnd)
    UI.SetWindowText(hWndCryptoOutput, "Encrypted Coordinates: \n")
    UI.SendMessage(hwnd, con.WM_SETFONT, hFont, False)
    UI.SetWindowPos(hwnd, 0, 0, 0, 1000, 575, con.SWP_NOMOVE | con.SWP_NOZORDER)

def initProgram(hwnd):
    global coords
    global encrypted
    global encryptedMsg
    dim = win.getBmpDimensions(hBmp)        # [width, height]
    rect = (BMP_XCOORD, BMP_YCOORD, dim[0], dim[1])
    coords = cpt.generateCoords(rect, 4)
    setFirstCoordinate(coords)
    strCoords = cpt.pointsToStr(coords)
    encrypted = cpt.encryptWords(strCoords)
    encryptedMsg = cpt.strArrToString(encrypted)

def setEncryptedMsg():
    wndText = UI.GetWindowText(hWndCryptoOutput)
    wndText += encryptedMsg
    UI.SetWindowText(hWndCryptoOutput, wndText)


def cleanUp():
    UI.DestroyWindow(hWndInputX)
    UI.DestroyWindow(hWndInputY)
    UI.DestroyWindow(hWndCoordBtn)
    UI.DeleteObject(hFont)
    UI.DeleteObject(hBmp)

def repaintWindow(hdc, ps):
    UI.FillRect(hdc, ps[2], UI.GetStockObject(con.WHITE_BRUSH))

    if not win.loadBMPIntoDC(hdc, hBmp, BMP_XCOORD, BMP_YCOORD):
        raise SystemError("Failed to load bmp")

    oldHPB = UI.SelectObject(hdc, UI.GetStockObject(con.BLACK_BRUSH))
    win.drawCircle(hdc, xCoord, yCoord, 20)
    UI.SelectObject(hdc, oldHPB)


def setFont():
    UI.SendMessage(hWndCoordBtn, con.WM_SETFONT, hFont, True)
    UI.SendMessage(hWndInputX, con.WM_SETFONT, hFont, True)
    UI.SendMessage(hWndInputY, con.WM_SETFONT, hFont, True)
    UI.SendMessage(hWndCryptoOutput, con.WM_SETFONT, hFont, True)

def processMovBtnClick(hwnd):
    global xCoord
    global yCoord
    xCStr = UI.GetWindowText(hWndInputX)
    yCStr = UI.GetWindowText(hWndInputY)
    dims = win.getBmpDimensions(hBmp)
    status = validateBtnInput(xCStr, yCStr, dims)
    if status == STATUS_OK:
        xCoord = int(xCStr)
        yCoord = int(yCStr)
        rect = UI.GetClientRect(hwnd)
        UI.RedrawWindow(hwnd, rect, 0, con.RDW_INVALIDATE | con.RDW_INTERNALPAINT)
    elif status == STATUS_INPUT_OUTOF_RANGE:
        UI.MessageBox(hwnd, "The specified coordinates are out of range.", "Error", con.MB_OK | con.MB_ICONEXCLAMATION)
    else:
        UI.MessageBox(hwnd, "Invalid input!", "Error", con.MB_OK | con.MB_ICONEXCLAMATION)

# ##################################################################
# ##################################################################

# wndProc gets calles by the OS every single time the windows is repainted. All drawing must be done below WM_PAINT.
# painting has to be done fast so that the window doesn't stop responding, or lag

def wndProc(hwnd, uMsg, wParam, lParam):
    global hBmp
    global windowCreated
    global hWndInputX
    global hWndInputY
    global hWndCoordBtn
    global hWndCryptoOutput
    global hFont
    global xCoord
    global yCoord

    if uMsg == con.WM_CREATE:                   # Python buf: WM_CREATE never gets called, use sendmessage

        initWindow(hwnd)
        initProgram(hwnd)
        setEncryptedMsg()
        return 0

    elif uMsg == con.WM_CLOSE:

        cleanUp()
        UI.DestroyWindow(hwnd)
        return 0

    elif uMsg == con.WM_DESTROY:                        # trigerred when DestroyWindow is called

        UI.PostQuitMessage(0)
        return 0
    elif uMsg == con.WM_QUIT:                           # triggered when PostQuitMessage is called, but it's not called as it's supposed to...

        return 0
    elif uMsg == con.WM_SIZE:                           # recompute the sizes of each component to be painted. This event is called when the window is resized

        return 0
    elif uMsg == con.WM_PAINT:

        if not windowCreated:
            UI.SendMessage(hwnd, con.WM_CREATE, 0, 0)  # This must be done once manually, since there is a bug PyWin32
            windowCreated = True
            return 0

        hDC, paintStruct = UI.BeginPaint(hwnd)  # returns handle to the device context and the paint structure

        try:
            repaintWindow(hDC, paintStruct)
        except SystemError:
            UI.EndPaint(hwnd, paintStruct)
            UI.PostQuitMessage(-1)
            return -1

        UI.EndPaint(hwnd, paintStruct)  # resources must be released when painting is done
        return 0

    elif uMsg == con.WM_COMMAND:

        if UI.LOWORD(wParam) == ID_COORDBTN:
            processMovBtnClick(hwnd)

        return 0

    elif uMsg == con.WM_SETFONT:

        setFont()
        return 0

    else:
        return UI.DefWindowProc(hwnd, uMsg, wParam, lParam)     # if msg handler is not defined, then do nothing

# end of function



# Program entry

def main():
    file = f.File("test.txt", True, False)
    fData = file.getFileData()
    print(fData)
    print(fData[0])             # 82 is the ascii code for R

    window = win.WNDClass(wndProc)
    window.setResizable(False)
    window.createWindow("Crypto-Crack")
    window.start()


# start the program
main()




