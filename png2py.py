import base64
import io
import sys
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtWidgets import QWidget,QLabel,QHBoxLayout

def pic_to_py(path_):
    """
    将图像文件转换为py文件
    :param path_:
    :return:
    """
    import base64

    with open(path_, "rb") as f:
        read_pic = f.read()

    b64str = base64.b64encode(read_pic)

    write_data = "img = " + '"' + b64str.decode("utf-8") + '"'
    print(write_data)

    write_path = path_.replace('.', '_') + ".py"
    with open(write_path, "w+") as f:
        f.write(write_data)

if __name__ == "__main__":
 
    path = "d:\zfm.png"  # 文件写入路径
    pic_to_py(path)

    print("convert png to py ok!")


# class MyQrWidget(QWidget):
#     def __init__(self):
#         super(MyQrWidget, self).__init__()

#         import base64
#         from PIL import Image,ImageQt
#         from zfm_png import img as app_png

#         pil_img = Image.open(io.BytesIO(base64.b64decode(app_png)))
#         pp = ImageQt.toqpixmap(pil_img)


#         self.setWindowTitle(u"您的帮助，使我进步！")
#         self.hbox = QHBoxLayout (self)
#         #pp = 'd:\zfm.png'
            
#         label = QLabel()
#         label.setPixmap(QtGui.QPixmap(pp))
#         label.setScaledContents(True)

#         self.hbox.addWidget(label)

# if __name__ == "__main__":
 

#     app = QtWidgets.QApplication(sys.argv)

#     myWin = MyQrWidget()
#     myWin.show()

#     # pp = 'd:\zfm.png'
#     # qimage = QtGui.QPixmap(pp).toImage()
#     # print (qimage)

#     # qbytearray = QtCore.QByteArray()
#     # buf = QtCore.QBuffer(qbytearray)
#     # buf.open(QtCore.QIODevice.WriteOnly);
#     # qimage.save(buf,"png");
#     # print ("=========sart=============")
#     # print (base64.b64encode(buf.data()))
#     # print ("=========end=============")

#     # with open('d:\p.txt', 'wb') as f:
#     #     f.write(base64.b64encode(buf.data()))

#     #path = "d:\zfm.png"  # 文件写入路径
#     #pic_to_py(path)


# # import base64
# # from app_png import img as app_png

# # bs4 = base64.b64decode(app_png)
# # print(type(bs4))

# # tmp = open('new_app.png', 'wb+')
# # tmp.write(bs4)
# # tmp.close()

#     sys.exit(app.exec_())

# import sys
# from PyQt5 import QtGui,QtWidgets,QtCore

# from donate import MyQrWidget as Qr 

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)

#     myWin = Qr()
#     myWin.show()
#     sys.exit(app.exec_())
