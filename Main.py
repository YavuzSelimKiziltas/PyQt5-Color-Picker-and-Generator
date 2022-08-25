import os
import sys
from colorPicker import Ui_Form
from os import environ
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
import pyautogui
from colorPicker import *
import re

###Convert UI to PyQt5 py file###
os.system("pyuic5 -o colorPicker.py colorPicker.ui")


environ["QT_DEVICE_PIXEL_RATIO"] = "0"
environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
environ["QT_SCREEN_SCALE_FACTORS"] = "1"
environ["QT_SCALE_FACTOR"] = "1"

class MainWindow(QMainWindow):


    def checkRgbCorrect(self,rgb):
        rgb = rgb.replace(" ","")

        matched = re.match('^\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])+,([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])+,([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])+\)+$',rgb)
        if bool(matched):
            matched = re.split(r'\D+',rgb)
            r = matched[1]
            g = matched[2]
            b = matched[3]
            return r,g,b
        else:
            return -1   

    def checkBgrCorrect(self,bgr):
        bgr = bgr.replace(" ","")

        matched = re.match('^\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])+,([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])+,([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])+\)+$',bgr)
        if bool(matched):
            matched = re.split(r'\D+',bgr)
            b = matched[1]
            g = matched[2]
            r = matched[3]
            return b,g,r
        else:
            return -1 
            
    def checkHexCorrect(self,hex):
        if len(hex) == 0:
            return False
        if (hex[0] != '#'):
            return False
 
        if (not(len(hex) == 7)):
            return False
 
        for i in range(1, len(hex)):
            if (not((hex[i] >= '0' and hex[i] <= '9') or (hex[i] >= 'a' and hex[i] <= 'f') or (hex[i] >= 'A' or hex[i] <= 'F'))):
                return False
 
        return True

    def checkHsvCorrect(self,hsv):
        hsv = hsv.replace(" ","")
        matched = re.split(r'\D+',hsv)
        if len(matched) != 5:
            return -1
        else:
            h = matched[1]
            s = matched[2]
            v = matched[3]

            if  (0 <= int(h) <= 360) and (0 <= int(s) <= 100) and (0 <= int(v) <= 100):
                return h,s,v
            else:
                return -1
    
    def getfiles(self):

        if  os.stat(os.path.join("assets", "LastFilePath.dat")).st_size == 0:
            lastFilePath = open(os.path.join("assets", "LastFilePath.dat"), "w")
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Image files (*.png *.jpg *.bmp)', os.getcwd())
            lastFilePath.write(os.path.abspath(os.path.join(fileName, os.pardir)))
            lastFilePath.close()
        else:
            lastFilePath = open(os.path.join("assets", "LastFilePath.dat"), "r")
            #print(f" Not Empty -> {lastFilePath.read()}")
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Images (*.png *.jpg .*jpeg)', lastFilePath.read())
            lastFilePath.close()
            lastFilePath = open(os.path.join("assets", "LastFilePath.dat"), "w")
            lastFilePath.write(os.path.abspath(os.path.join(fileName, os.pardir)))
            
        if fileName.endswith(".png") or fileName.endswith(".jpg") or fileName.endswith(".jpeg"):
            self.pixmap = QPixmap(fileName)
            self.ui.PictureLabel.setPixmap(self.pixmap)
            self.ui.PictureLabel.setScaledContents(True)
        else:
            self.show_popup("This file type is not supported!")

    def show_popup(self,text):
        msg = QMessageBox.warning(self, "Error", text)

    def on_combobox_changed(self, value):
        if value == "RGB":
            self.ui.generateLine.setPlaceholderText("(125,200,60)")
        if value == "BGR":
            self.ui.generateLine.setPlaceholderText("(100,150,90)")
        if value == "HEX":
            self.ui.generateLine.setPlaceholderText("#AED6F1")
        if value == "HSV":
            self.ui.generateLine.setPlaceholderText("(270,84,43)")
            

    def generateColor(self):
        colorType = self.ui.colorComboBox.currentText()
        colorCode = self.ui.generateLine.text()
        
        if colorType=="RGB" and (self.checkRgbCorrect(colorCode) != -1):
            r,g,b = self.checkRgbCorrect(colorCode)
            self.ui.colorPaletteWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 1px solid black;")
            self.ui.mouseCurrentWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 1px solid black;")
            hex = self.rgb_to_hex(int(r), int(g), int(b))
            h, s, v = self.rgb_to_hsv(int(r), int(g), int(b))
            self.ui.HexLabel.setText(hex)
            self.ui.RgbLabel.setText(f"({r},{g},{b})")
            self.ui.BgrLabel.setText(f"({b},{g},{r})")
            self.ui.HsvLabel.setText(f"({int(h)},{int(s)},{int(v)})")

        elif colorType=="BGR" and (self.checkBgrCorrect(colorCode) != -1):
            b,g,r = self.checkBgrCorrect(colorCode)
            self.ui.colorPaletteWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 1px solid black;")
            self.ui.mouseCurrentWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 1px solid black;")
            hex = self.rgb_to_hex(r,g,b)
            h, s, v = self.rgb_to_hsv(int(r), int(g), int(b))
            self.ui.HexLabel.setText(hex)
            self.ui.RgbLabel.setText(f"({r},{g},{b})")
            self.ui.BgrLabel.setText(f"({b},{g},{r})")
            self.ui.HsvLabel.setText(f"({int(h)},{int(s)},{int(v)})")

        elif colorType=="HEX" and self.checkHexCorrect(colorCode):
            self.ui.colorPaletteWidget.setStyleSheet(f"background: {colorCode}; border: 1px solid black;")
            self.ui.mouseCurrentWidget.setStyleSheet(f"background: {colorCode}; border: 1px solid black;")
            r,g,b = self.hex_to_rgb(colorCode)
            bgr = f"({b}, {g}, {r})"
            self.ui.RgbLabel.setText(f"({r},{g},{b})")
            self.ui.BgrLabel.setText(f"({b},{g},{r})")
            self.ui.HexLabel.setText(colorCode)
            h, s, v = self.rgb_to_hsv(int(r), int(g), int(b))
            self.ui.HsvLabel.setText(f"({int(h)},{int(s)},{int(v)})")

        elif colorType=="HSV" and (self.checkHsvCorrect(colorCode) != -1):
            h,s,v = self.checkBgrCorrect(colorCode)
            r,g,b = self.hsv_to_rgb(int(h),int(s),int(v))
            self.ui.colorPaletteWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 1px solid black;")
            self.ui.mouseCurrentWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 1px solid black;")
            hex = self.rgb_to_hex(r,g,b)
            self.ui.HexLabel.setText(hex)
            self.ui.RgbLabel.setText(f"({r},{g},{b})")
            self.ui.BgrLabel.setText(f"({b},{g},{r})")
            self.ui.HsvLabel.setText(f"({int(h)},{int(s)},{int(v)})")

        else:
            self.show_popup("Please check your color code again")

    def copyToClipBoard(self, colorType):
        if colorType == 0:
            self.ui.colorComboBox.setCurrentIndex(colorType)
            global content
            content = self.ui.RgbLabel.text()
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(content, mode = cb.Clipboard)
            self.ui.generateLine.setText(content)
            
        elif colorType == 1:
            self.ui.colorComboBox.setCurrentIndex(colorType)
            content = self.ui.BgrLabel.text()
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(content, mode = cb.Clipboard)
            self.ui.generateLine.setText(content)
            
        elif colorType == 2:
            self.ui.colorComboBox.setCurrentIndex(colorType)
            content = self.ui.HexLabel.text()
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(content, mode = cb.Clipboard)
            self.ui.generateLine.setText(content)
            
        elif colorType == 3:
            self.ui.colorComboBox.setCurrentIndex(colorType)
            content = self.ui.HsvLabel.text()
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(content, mode = cb.Clipboard)
            self.ui.generateLine.setText(content)
           
    def mousePressEvent(self, event):
        self.click = 1
        self.update()

    def mouseReleaseEvent(self, event):
        self.click = 0
        self.update()

    def rgb_to_hsv(self, r, g, b):
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = (df/mx)*100
        v = mx*100
        return h, s, v

    def _hsv2rgb(self,h, s, v):
        if s == 0.0:
            return v, v, v
        i = int(h*6.0) # XXX assume int() truncates!
        f = (h*6.0) - i
        p = v*(1.0 - s)
        q = v*(1.0 - s*f)
        t = v*(1.0 - s*(1.0-f))
        i = i%6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q

    def hsv_to_rgb(self,h,s,v):
        (h, s, v) = (h / 360, s / 100, v / 100)
        (r, g, b) = self._hsv2rgb(h, s, v)
        (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))
        return r,g,b

    def rgb_to_hex(self,r,g,b):
        r = int(r)
        g = int(g)
        b = int(b)
        return '#%02X%02X%02X' % (r, g, b)

    def hex_to_rgb(self,hex):
        rgb = []
        hex = hex.lstrip('#')
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)

        return rgb

    def checkMouse(self):
        is_under = self.ui.PictureLabel.underMouse()
        if is_under and self.click == 0:
            x, y = pyautogui.position()
            pixelColor = pyautogui.screenshot().getpixel((x, y))
            r, g, b = (pixelColor[0]), (pixelColor[1]), (pixelColor[2])               
            self.ui.mouseCurrentWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 2px solid black;")
        elif is_under and self.click == 1:
            x, y = pyautogui.position()
            pixelColor = pyautogui.screenshot().getpixel((x, y))
            r, g, b = (pixelColor[0]), (pixelColor[1]), (pixelColor[2])
            self.ui.RgbLabel.setText(f"({(pixelColor[0])}, {(pixelColor[1])}, {(pixelColor[2])})")
            self.ui.BgrLabel.setText(f"({(pixelColor[2])}, {(pixelColor[1])}, {(pixelColor[0])})")
            hex = self.rgb_to_hex(int(pixelColor[0]), int(pixelColor[1]), int(pixelColor[2]))
            self.ui.HexLabel.setText(hex)
            h, s, v = self.rgb_to_hsv(r,g,b)
            self.ui.HsvLabel.setText(f"({int(h)},{int(s)},{int(v)})")
            self.ui.colorPaletteWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 2px solid black;")
            self.ui.mouseCurrentWidget.setStyleSheet(f"background: rgb({r},{g},{b}); border: 2px solid black;")
            self.update()

    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.PictureLabel.setCursor(Qt.CrossCursor)
        self.setFixedHeight(680)
        self.setFixedWidth(1016)
        self.ui.rgbCopy.setToolTip("Copy content to clipboard")
        self.ui.bgrCopy.setToolTip("Copy content to clipboard")
        self.ui.hexCopy.setToolTip("Copy content to clipboard")
        self.ui.hsvCopy.setToolTip("Copy content to clipboard")
        self.ui.fileBrowserWidget.setToolTip("You can browse to your own image")
        self.ui.mouseCurrentWidget.setToolTip("Current mouse location")
        self.ui.colorPaletteWidget.setToolTip("Last mouse Click")
        

        self.click = 0

        timer = QTimer(self)
        timer.timeout.connect(self.checkMouse)
        timer.start(100)

        self.ui.rgbCopy.setIcon(QIcon(os.path.join("assets","copyIcon.png")))
        self.ui.bgrCopy.setIcon(QIcon(os.path.join("assets","copyIcon.png")))
        self.ui.hexCopy.setIcon(QIcon(os.path.join("assets","copyIcon.png")))
        self.ui.hsvCopy.setIcon(QIcon(os.path.join("assets","copyIcon.png")))
        self.ui.fileBrowserButton.setIcon(QIcon(os.path.join("assets","fileBrowserIcon.png")))
        self.ui.fileBrowserButton.setIconSize(QSize(50, 50))

        self.pixmap = QPixmap(os.path.join("assets","Sample.jpg"))
        self.ui.PictureLabel.setPixmap(self.pixmap)
        self.ui.PictureLabel.setScaledContents(True)
        self.ui.colorComboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.ui.rgbCopy.clicked.connect(lambda: self.copyToClipBoard(colorType = 0))
        self.ui.bgrCopy.clicked.connect(lambda: self.copyToClipBoard(colorType = 1))
        self.ui.hexCopy.clicked.connect(lambda: self.copyToClipBoard(colorType = 2))
        self.ui.hsvCopy.clicked.connect(lambda: self.copyToClipBoard(colorType = 3))
        self.ui.fileBrowserButton.clicked.connect(lambda: self.getfiles())
        self.ui.generateButton.clicked.connect(lambda: self.generateColor())
        self.ui.PictureLabel.setStyleSheet("background: white; color: black; ")
        self.ui.generateButton.setShortcut("Return")
        
        self.ui.colorPaletteWidget.setStyleSheet("background-color: white; border: 2px solid black;",)
        self.ui.mouseCurrentWidget.setStyleSheet("background-color: white; border: 2px solid black;",)

        self.ui.generateLine.setPlaceholderText("(125,200,60)")

        self.ui.rgbCopyWidget.setStyleSheet("border: none;")
        self.ui.RgbLabel.setStyleSheet("border: None;")
        self.ui.rgbCopy.setStyleSheet("border: None;")
        self.ui.label1.setStyleSheet("border: None;")

        self.ui.bgrCopyWidget.setStyleSheet("border: none;")
        self.ui.BgrLabel.setStyleSheet("border: None;")
        self.ui.bgrCopy.setStyleSheet("border: None;")
        self.ui.label2.setStyleSheet("border: None;")

        self.ui.hexCopyWidget.setStyleSheet("border: none;")
        self.ui.HexLabel.setStyleSheet("border: None;")
        self.ui.hexCopy.setStyleSheet("border: None;")
        self.ui.label3.setStyleSheet("border: None;")
        
        self.ui.hsvCopyWidget.setStyleSheet("border: none;")
        self.ui.HsvLabel.setStyleSheet("border: None;")
        self.ui.hsvCopy.setStyleSheet("border: None;")
        self.ui.label4.setStyleSheet("border: None;")

        def on_timeout():
            self.ui.label.setVisible(False)
            self.ui.label_2.setVisible(False)

        QtCore.QTimer.singleShot(1500, on_timeout)

        self.ui.colorComboBox.setStyleSheet(            """
            background: white;
            border : 1px solid black;
            border-top-left-radius : 5px;
            border-top-right-radius : 5px;
            border-bottom-left-radius:5px;
            border-bottom-right-radius : 5px;
            """
            )

        self.ui.fileBrowserWidget.setStyleSheet(            """
            background: #AED6F1;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
            )

        self.ui.generateButtonWidget.setStyleSheet(            """
            background: white;
            color: black;
            border: none;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
            )

        self.ui.generateLineWidget.setStyleSheet(            """
            background: white;
            color: black;
            border: none;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
            )

        self.ui.generateFrame.setStyleSheet(            """
            background: #C4DFAA;
            border: 1px solid black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(20)
            )

        self.ui.rgbCopyWidget.setStyleSheet(            """
            background: white;
            color: black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
        )

        self.ui.hsvCopyWidget.setStyleSheet(            """
            background: white;
            color: black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
        )

        self.ui.bgrCopyWidget.setStyleSheet(            """
            background: white;
            color: black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
        )

        self.ui.hexCopyWidget.setStyleSheet(            """
            background: white;
            color: black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
        )

        self.ui.HexWidget.setStyleSheet(            """
            background: #C4DFAA;
            border: 1px solid black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(20)
        )

        self.ui.HsvWidget.setStyleSheet(            """
            background: #C4DFAA;
            border: 1px solid black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(20)
        )

        self.ui.RgbWidget.setStyleSheet(            """
            background: #C4DFAA;
            border: 1px solid black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(20)
        )

        self.ui.BgrWidget.setStyleSheet(            """
            background: #C4DFAA;
            border: 1px solid black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(20)
        )

        self.ui.Frame.setStyleSheet(            """
            background: #AED6F1;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(20)
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Color Picker")
    window.setWindowIcon(QIcon(os.path.join("assets","WindowIcon.png")))
    window.show()
    sys.exit(app.exec_())