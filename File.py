
import win32con as con
import win32file as wf
import winerror

class File:

    def __init__(self, fileName, isReadOnly, isShared):
        self.hFile = self.createFile(fileName, isReadOnly, isShared)
        self.validateHandle()
        self.data = self.readFile()

    def __del__(self):
        wf.CloseHandle(self.hFile)

    def createFile(self, fName, isReadOnly, isShared):
        shareMode = 0
        access = 0
        if isShared:
            shareMode = con.FILE_SHARE_WRITE
        else:
            shareMode = con.FILE_SHARE_READ

        if isReadOnly:
            access = con.GENERIC_READ
        else:
            access = con.GENERIC_WRITE
        return wf.CreateFile(fName, access, shareMode, None, con.OPEN_ALWAYS, 0, 0)

    def validateHandle(self):
        if self.hFile == wf.INVALID_HANDLE_VALUE:
            raise winerror.ERROR_INVALID_HANDLE

    def readFile(self):
        fileSize = wf.GetFileSize(self.hFile)
        wf.SetFilePointer(self.hFile, 0, wf.FILE_BEGIN)
        result, fData = wf.ReadFile(self.hFile, fileSize, None)
        if result:
            return 0
        return fData


    def getFileData(self):
        return self.data



