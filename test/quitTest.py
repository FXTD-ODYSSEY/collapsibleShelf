from Qt import QtCore
from Qt import QtWidgets


path = r"D:\Users\82047\Desktop\test\test.txt"
def quitEvent():
    print path
    with open(path,'w') as f:
        f.write("hello")

QtWidgets.QApplication.instance().aboutToQuit.connect(quitEvent)