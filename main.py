
import Windows
import File as f
import string



def main():
    file = f.File("test.txt", True, False)
    fData = file.getFileData()
    print(fData)
    print(fData[0])             # 82 is the ascii code for R

    window = Windows.WNDClass()
    window.createWindow("Crypto-Crack")
    window.start()

main()

