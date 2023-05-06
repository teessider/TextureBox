import sys

from PySide2 import QtWidgets


class TextureBoxMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(TextureBoxMainWindow, self).__init__()

        self.setObjectName(self.__class__.__name__)
        self.setWindowTitle("Texture Box")

        self.show()


if __name__ == '__main__':
    try:
        TextureBoxApp = QtWidgets.QApplication(sys.argv)
        TextureBox = TextureBoxMainWindow()
        TextureBoxApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error: ", sys.exc_info()[1])
    except SystemExit:
        print("Closing TextureBox Window...")
