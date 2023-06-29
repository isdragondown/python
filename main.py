# 开发第一个基于PyQt5的桌面应用
from PyQt5.QtGui import QPixmap
import sys
import consume

from PyQt5.QtWidgets import *

if __name__ == '__main__':
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    # 创建一个窗口
    w = QWidget()
    # 设置窗口尺寸   宽度300，高度150
    w.resize(400, 200)
    # 移动窗口
    w.move(150,100)

    # 设置窗口的标题
    w.setWindowTitle('第一个基于PyQt5的桌面应用')

    consume = consume.Ui_Form()
    consume.setupUi(w)

    # 显示窗口0
    w.show()

    
    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())


