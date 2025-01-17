# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'name.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from scapy.layers.inet import ICMP, IP, TCP, sr1
import socket
import os

logo = "Synscan-logo.jpg"
path = os.path.dirname(os.path.realpath(__file__))
address = os.path.join(path, logo)

class Ui_MainWindow(object):
    def scan_target(self):
        def icmp_probe(ip):  # Здесь производится проверка на наличие сервера в сети
            icmp_packet = IP(dst=ip) / ICMP()
            resp_packet = sr1(icmp_packet, timeout=5)  # Отправка и прием одного пакета
            return resp_packet is not None

        def syn_scan(ip, ports):  # В данном месте проводится сканирование путем отправки пакетов
            for port in ports:  # Проходимся по каждому порту и отправляем TCP пакет
                syn_packet = IP(dst=ip) / TCP(dport=port, flags="S")  # Флаг S означает SYN пакет
                resp_packet = sr1(syn_packet, timeout=10)  # Время ожидания пакета можно ставить свое
            
                if resp_packet is not None:
                   if resp_packet.getlayer('TCP').flags == 0x12: # проверить, открыт ли порт
                        print(f"{ip}:{port} is open/{resp_packet.sprintf('%TCP.sport%')}")
                        self.check_textEdit.append(f"{ip}:{port} is open/{resp_packet.sprintf('%TCP.sport%')}")
                   if resp_packet.getlayer(TCP).flags == 0x14:# проверить, закрыт ли порт
                        print(f"{ip}:{port} is closed/{resp_packet.sprintf('%TCP.sport%')}")
                        self.check_textEdit.append(f"{ip}:{port} is closed/{resp_packet.sprintf('%TCP.sport%')}")
                else :
                     # если ответ не получен, считается, что порт отфильтрован.
                     # Фильтрованный порт - это порт, который блокируется или фильтруется брандмауэром или 
                     # другим механизмом безопасности в системе или сети.
                     print(f"{ip}:{port} is filtered")
                     self.check_textEdit.append(f"{ip}:{port} is filtered")
                     
        if __name__ == "__main__":
            name = self.ip_lineEdit.text()  # Задаем цель (без http/https)
            if self.ip_lineEdit.text() == "":
                inf = QMessageBox()
                inf.setWindowTitle("WARNING")
                inf.setText(f"You haven't entered a value!")
                inf.setIcon(QMessageBox.Warning)
                inf.setStandardButtons(QMessageBox.Ok)
                inf.exec_()
                raise SystemExit
            else:
                pass
            ip = socket.gethostbyname(name)  # Узнаем IP цели
            self.check_textEdit.clear()
            self.check_textEdit.append(f"Target: {ip}")
            ports = [20, 21, 22, 23, 25, 43, 53, 80,  # Обозначаем порты для сканирования
                     115, 123, 143, 161, 179, 443, 445,
                     514, 515, 993, 995, 1080, 1194,
                     1433, 1723, 3128, 3268, 3306, 3389,
                     5432, 5060, 5900, 8080, 10000]
            try:  # Перехватываем исключения в момент, когда заканчивается кортеж
                if icmp_probe(ip):  # Если не удалось подключиться к серверу выводим ошибку
                    syn_ack_packet = syn_scan(ip, ports)
                    syn_ack_packet.show()
                else:
                    self.check_textEdit.append("Failed to send ICMP package")
            except AttributeError:
                self.check_textEdit.append("Scan completed!")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 350)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(3, 3, 3);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"),
                       QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ip_label = QtWidgets.QLabel(self.centralwidget)
        self.ip_label.setGeometry(QtCore.QRect(20, 110, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ip_label.setFont(font)
        self.ip_label.setStyleSheet("color: rgb(205, 254, 2);")
        self.ip_label.setObjectName("ip_label")
        self.ip_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_lineEdit.setGeometry(QtCore.QRect(120, 110, 161, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.ip_lineEdit.setFont(font)
        self.ip_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ip_lineEdit.setObjectName("ip_lineEdit")
        self.check_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.check_textEdit.setGeometry(QtCore.QRect(20, 140, 500, 111))
        self.check_textEdit.setStyleSheet("color: rgb(255, 255, 255);\n"
                                          "background-color: rgb(32, 34, 33);")
        self.check_textEdit.setObjectName("check_textEdit")
        self.start_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.start_pushButton.setGeometry(QtCore.QRect(90, 270, 121, 51))
        self.start_pushButton.clicked.connect(self.scan_target)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(True)
        font.setPointSize(11)
        font.setWeight(75)
        self.start_pushButton.setFont(font)
        self.start_pushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "background-color: rgb(205, 254, 2);")
        self.start_pushButton.setObjectName("start_pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 300, 100))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(address))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SYNScan"))
        self.ip_label.setText(_translate("MainWindow", "IP ADDRESS"))
        self.start_pushButton.setText(_translate("MainWindow", "START"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
