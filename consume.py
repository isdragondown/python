from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
import json
import shutil



class Ui_Form(object):
    #控件位置
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 500)


        #背景图片，通过label控件覆盖背景
        self.label = QtWidgets.QLabel(Form)
        bg_image = QPixmap("壁纸.png")
        self.label.setPixmap(bg_image.scaled(1000, 500))
        self.label.resize(1000, 500)
    
        

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(470, 100, 101, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 370, 131, 81))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(470, 190, 101, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(470, 280, 101, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_bg = QtWidgets.QPushButton(Form)
        self.pushButton_bg.setGeometry(QtCore.QRect(20, 320, 131, 31))
        self.pushButton_bg.setObjectName("pushButton_bg")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 30, 71, 21))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        self.calendarWidget.setGeometry(QtCore.QRect(20, 100, 251, 201))
        self.calendarWidget.setObjectName("calendarWidget")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 230, 111, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(300, 101, 71, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(300, 210, 54, 12))
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(300, 130, 104, 71))
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(40, 50, 151, 31))
        self.textBrowser.setObjectName("textBrowser")

        #控件点击
        self.retranslateUi(Form)
        self.pushButton_2.clicked.connect(Form.close) # type: ignore
        self.pushButton.clicked.connect(self.add_expense) # type: ignore
        self.pushButton_3.clicked.connect(self.add_income) # type: ignore
        self.pushButton_4.clicked.connect(self.show_detail_window) # type: ignore
        self.pushButton_bg.clicked.connect(self.select_background_image) #背景选取事件
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.load_data()

    #控件默认状态
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "收支系统"))
        self.pushButton.setText(_translate("Form", "消费"))
        self.pushButton_2.setText(_translate("Form", "退出"))
        self.pushButton_3.setText(_translate("Form", "收入"))
        self.pushButton_4.setText(_translate("Form", "明细"))
        self.pushButton_bg.setText(_translate("Form","选择背景图片"))
        self.label.setText(_translate("Form", "当前余额："))
        self.lineEdit_2.setText(_translate("Form", "0"))
        self.label_2.setText(_translate("Form", "说明："))
        self.label_3.setText(_translate("Form", "金额："))

    #读取data.json文件信息，不存在或异常则以默认状态重新
    def load_data(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                self.balance = data["balance"]
                self.expenses = data["expenses"]
                self.incomes = data["incomes"]
        except:
            self.balance = 0
            self.expenses = []
            self.incomes = []

        self.update_balance()

    #保存数据到data中
    def save_data(self):
        data = {
            "balance": self.balance,
            "expenses": self.expenses,
            "incomes": self.incomes
        }
        with open("data.json", "w") as f:
            json.dump(data, f)

    #更新余额信息
    def update_balance(self):
        self.textBrowser.setText("{}".format(self.balance))
        self.lineEdit_2.setText("")
        self.textEdit.setText("")

    #收入函数
    def add_income(self):
        if self.lineEdit_2 == 0 or self.lineEdit_2:
            self.update_balance()
            return
        amount = float(self.lineEdit_2.text())
        description = self.textEdit.toPlainText()
        self.incomes.append({"amount": amount, "description": description})
        self.balance += amount
        self.update_balance()
        self.save_data()
    #消费函数
    def add_expense(self):
        if self.lineEdit_2 == 0 or self.lineEdit_2:
            self.update_balance()
            return
        amount = float(self.lineEdit_2.text())
        description = self.textEdit.toPlainText()
        self.expenses.append({"amount": amount, "description": description})
        self.balance -= amount
        self.update_balance()
        self.save_data()

    #明细窗口
    def show_detail_window(self):
        self.detail_window = DetailWindow(self.expenses, self.incomes)
        self.detail_window.show()

    # 背景函数
    def select_background_image(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "选择背景图片", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            new_file_path = "./壁纸.png"  # 新文件路径和名称
            shutil.copy(file_path, new_file_path)  # 复制文件
            self.show_restart_dialog()

    def show_restart_dialog(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("提示")
        message_box.setText("背景图片已更改，需要重启窗口以应用更改。")
        message_box.addButton(QMessageBox.Ok)
        message_box.exec_()
            
class DetailWindow(QtWidgets.QWidget):
    def __init__(self, expenses, incomes):
        #调用父窗口的默认设置
        super().__init__()
        self.setWindowTitle("明细")

        self.expenses = expenses
        self.incomes = incomes

        #创建两控件
        self.expense_list = QtWidgets.QListWidget()
        self.income_list = QtWidgets.QListWidget()

        self.update_lists()

        #创建两Label控件
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(QtWidgets.QLabel("支出："))
        vbox.addWidget(self.expense_list)
        vbox.addWidget(QtWidgets.QLabel("收入："))
        vbox.addWidget(self.income_list)

        self.setLayout(vbox)

    #导入数据到控件中
    def update_lists(self):
        self.expense_list.clear()
        for expense in self.expenses:
            self.expense_list.addItem("{} 元 - {}".format(expense["amount"], expense["description"]))

        self.income_list.clear()
        for income in self.incomes:
            self.income_list.addItem("{} 元 - {}".format(income["amount"], income["description"]))


