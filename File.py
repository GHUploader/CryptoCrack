
import win32con as con
import win32file as wf
import winerror

def fileExists(fileName):
    if not fileName:
        return False
    exists = True
    try:
        file = File(fileName, True, mustExist=True)
    except winerror.ERROR_INVALID_HANDLE:
        exists = False
    return exists


class File:

    def __init__(self, fileName, isReadOnly, isShared = False, mustExist = False):
        self.hFile = self.createFile(fileName, isReadOnly, isShared, mustExist)
        self.validateHandle()

        self.isOpen = True
        self.data = self.readFile()

        if isReadOnly:
            wf.CloseHandle(self.hFile)
            self.isOpen = False

    def __del__(self):
        if self.isOpen:
            wf.CloseHandle(self.hFile)

    def createFile(self, fName, isReadOnly, isShared, mustExist):
        shareMode = con.FILE_SHARE_READ
        access = con.GENERIC_WRITE
        cDisposition = con.OPEN_ALWAYS
        if isShared:
            shareMode = con.FILE_SHARE_WRITE

        if isReadOnly:
            access = con.GENERIC_READ

        if mustExist:
            cDisposition = con.OPEN_EXISTING

        return wf.CreateFile(fName, access, shareMode, None, cDisposition, 0, 0)

    def validateHandle(self):
        if self.hFile == wf.INVALID_HANDLE_VALUE:
            raise winerror.ERROR_INVALID_HANDLE

    def readFile(self):
        if not self.isOpen:
            return 0
        fileSize = wf.GetFileSize(self.hFile)
        wf.SetFilePointer(self.hFile, 0, wf.FILE_BEGIN)
        result, fData = wf.ReadFile(self.hFile, fileSize, None)
        if result:
            return 0
        return fData


    def getFileData(self):
        return self.data



