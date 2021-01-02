#!/usr/bin/env python3

import io
import os
import sys

import pyperclip
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon,qApp,QMenu,QAction

from system_hotkey import SystemHotkey
from PyQt5.QtCore import QObject,pyqtSignal

# try:
#     from pynotifier import Notification
# except ImportError:
#     pass

#捐助
from donate import MyQrWidget as Qr 

#切换baidu paddleocr
import numpy as np
from paddleocr import PaddleOCR

PADDLE_OCR = None

class Snipper(QtWidgets.QWidget):
    #定义一个热键信号
    sig_keyhot = pyqtSignal(str)

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.hk_capture, self.hk_exit = SystemHotkey(),SystemHotkey()
        self.hk_capture.register(('alt','c'),callback=lambda x:self.send_key_event("capture"))
        self.hk_exit.register(('alt','q'),callback=lambda x:self.send_key_event("exit"))
        self.sig_keyhot.connect(self.hotkey_process)

    #热键信号发送函数(将外部信号，转化成qt信号)
    def send_key_event(self,i_str):
        self.sig_keyhot.emit(i_str)

    def hotkey_process(self, i_str):
        if i_str == "capture":
            self.capture()
        elif i_str == "exit":
            self.quit()
        elif i_str == "donate":
            self.donate()
        else:
            pass
    
    def donate(self):
        self.donateWin = Qr()
        self.donateWin.show()
        global tp
        tp.show()

    def quit(self):
        print(f"INFO: quit capture")
        QtWidgets.QApplication.quit()

    def capture(self):
        print(f"INFO: start capture!")

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        self.show()
        
        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()
        self.screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos()).grabWindow(0)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(self.screen))
        self.setPalette(palette)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, self.width(), self.height())

        if self.start == self.end:
            return super().paintEvent(event)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(painter.background())
        painter.drawRect(QtCore.QRect(self.start, self.end))
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        self.start = self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        self.hide()
        QtWidgets.QApplication.processEvents()
        shot = self.screen.copy(QtCore.QRect(self.start, self.end))
        processImage_pdocr(shot)
        #QtWidgets.QApplication.quit()

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


# def processImage(img):
#     buffer = QtCore.QBuffer()
#     buffer.open(QtCore.QBuffer.ReadWrite)
#     img.save(buffer, "PNG")
#     pil_img = Image.open(io.BytesIO(buffer.data()))
#     buffer.close()

#     try:
#         #result = pytesseract.image_to_string(
#         #    pil_img, timeout=5, lang=(sys.argv[1] if len(sys.argv) > 1 else None)
#         #)
#         result = pytesseract.image_to_string(
#             pil_img, timeout=8, lang="eng+chi_sim"
#         )
#     except RuntimeError as error:
#         print(f"ERROR: An error occurred when trying to process the image: {error}")
#         notify(f"An error occurred when trying to process the image: {error}")
#         return

#     if result:
#         #result = ''.join(result.split(' '))
#         pyperclip.copy(result)
#         print(f'INFO: Copied "{result}" to the clipboard')
#         #notify(f'Copied "{result}" to the clipboard')
#         notify(f'识别结果已保存到剪贴板\n "{result}" ')
#     else:
#         print(f"INFO: Unable to read text from image, did not copy")
#         notify(f"Unable to read text from image, did not copy")

def processImage_pdocr(img):
    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QBuffer.ReadWrite)
    img.save(buffer, "PNG")
    pil_img = Image.open(io.BytesIO(buffer.data()))
    buffer.close()

    try:
        global PADDLE_OCR
        ocr_result = PADDLE_OCR.ocr(np.array(pil_img))
        ocr_result = [line[1][0] for line in ocr_result]
        result = '\n'.join(ocr_result)

    except RuntimeError as error:
        print(f"ERROR: An paddleocr error occurred when trying to process the image: {error}")
        notify(f"An error paddleocr occurred when trying to process the image: {error}")
        return

    if result:
        #result = ''.join(result.split(' '))
        pyperclip.copy(result)
        print(f'INFO: Copied "{result}" to the clipboard')
        #notify(f'Copied "{result}" to the clipboard')
        notify(f'识别结果已保存到剪贴板\n "{ len(result) > 0 and result[20:] or result }" ')
    else:
        print(f"INFO: Unable to read text from image, did not copy")
        notify(f"Unable to read text from image, did not copy")

def notify(msg):
    # try:
    #     Notification(title="scr2txt", description=msg, duration=5, icon_path=( os.path.dirname(os.path.abspath(__file__)) + '\\scr2txt.ico')).send()
    # except (SystemError, NameError):
    #     trayicon = QtWidgets.QSystemTrayIcon(
    #         QtGui.QIcon(
    #             QtGui.QPixmap.fromImage(QtGui.QImage(1, 1, QtGui.QImage.Format_Mono))
    #         )
    #     )
    #     trayicon.show()
    #     trayicon.showMessage("scr2txt", msg, QtWidgets.QSystemTrayIcon.NoIcon)
    #     trayicon.hide()
    global tp
    tp.show()
    tp.showMessage("scr2txt", msg, QtWidgets.QSystemTrayIcon.NoIcon)
    #tp.hide()
    
if __name__ == "__main__":
    # try:
    #     pytesseract.get_tesseract_version()
    # except EnvironmentError:
    #     notify(
    #         "Tesseract is either not installed or cannot be reached.\n"
    #         "Have you installed it and added the install directory to your system path?"
    #     )
    #     print(
    #         "ERROR: Tesseract is either not installed or cannot be reached.\n"
    #         "Have you installed it and added the install directory to your system path?"
    #     )
    #     sys.exit()
    
    #notify(u"\nAlt+C：开始识别\nAlt+Q：退出")

    model_path = os.path.dirname(os.path.abspath(__file__)) + r'\\model\\'
    PADDLE_OCR = PaddleOCR(use_gpu=False,det_model_dir=model_path+'det', cls_model_dir='', rec_model_dir=model_path+'rec', rec_char_dict_path=model_path+'ppocr_keys_v1.txt')

    #QtWidgets.QApplication.setQuitOnLastWindowClosed(False) 
    QtCore.QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    snipper = Snipper(window)
    snipper.show()
        
    # 在系统托盘处显示图标
    tp = QSystemTrayIcon(window)
    tp.setIcon(QIcon('scr2txt.ico'))
    tp.setToolTip(u'Alt+C截屏，Alt+Q退出')

    capAct = QAction('截屏(&Caputure)',triggered = lambda x:snipper.send_key_event('capture'))
    extAct = QAction('退出(&Quit)',triggered = lambda x: tp.setVisible(False) or snipper.send_key_event('exit'))
    donAct = QAction('捐助(&Donate)',triggered = lambda x: tp.setVisible(False) or snipper.send_key_event('donate'))

    tpMenu = QMenu()
    tpMenu.addAction(capAct)
    tpMenu.addAction(extAct)
    tpMenu.addAction(donAct)
    tp.setContextMenu(tpMenu)
    tp.show()

    notify(u"\nAlt+C：开始识别\nAlt+Q：退出")


    sys.exit(app.exec_())

