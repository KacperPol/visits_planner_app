from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QImage, QPixmap
import requests
import string

class Ui_Window_map(object):

    # Wyświetlenie optymalnej trasy i adresu domowego
    def wysw_opt(self, trasa_opt, koszt_trasy, adresy, dane_osob, adres_dom):
        self.textBrowser_trasa.clear()
        for i in range(0, len(trasa_opt)):
            trasa_opt[i] = int(trasa_opt[i])
        for i in range(len(trasa_opt)-1):
            if i == 0:
                self.textBrowser_trasa.append("Adres domowy [" + string.ascii_uppercase[i] + "]: " + str(adres_dom))
            else:
                tekstTrasa = string.ascii_uppercase[i] +  ": " + str(dane_osob[trasa_opt[i]]) + ", " + str(adresy[trasa_opt[i]]) #string.ascii_uppercase[i] + ":  Klient nr." + str(trasa_opt[i]) +
                self.textBrowser_trasa.append(tekstTrasa)
        # Czas dojazdów - koszt_trasy
        # Czas wizyt - każdy adres x1.5h
        # Czas parkowania i dojścia - każdy adres x1/3h (20min)
        calkowity_czas = koszt_trasy + ((len(trasa_opt)-2)*5400) + ((len(trasa_opt)-2)*1200)
        self.textBrowser_trasa.append(" ")
        self.textBrowser_trasa.append("Całkowity czas pracy i dojazdow wynosi: " + str(round((calkowity_czas/3600),2)) + " h")

    # Ustawienia okna aplikacji
    def setupUi(self, Window_map, URL_image, trasa_opt, koszt_trasy, adresy, dane_osob, adres_dom):
        Window_map.setObjectName("Window_map")
        Window_map.resize(1112, 518)
        self.centralwidget = QtWidgets.QWidget(Window_map)
        self.centralwidget.setObjectName("centralwidget")

        # Mapa z URL
        self.label_mapa = QtWidgets.QLabel(self.centralwidget)
        self.label_mapa.setGeometry(QtCore.QRect(10, 10, 641, 481))
        self.label_mapa.setFrameShape(QtWidgets.QFrame.Box)
        self.label_mapa.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_mapa.setText("")
        image = QImage()
        image.loadFromData(requests.get(URL_image).content)
        self.label_mapa.setPixmap(QPixmap(image))
        self.label_mapa.setScaledContents(True)
        self.label_mapa.setOpenExternalLinks(False)
        self.label_mapa.setObjectName("label_mapa")

        # Trasa po pacjentach
        self.textBrowser_trasa = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_trasa.setGeometry(QtCore.QRect(660, 10, 441, 481))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_trasa.setFont(font)
        self.textBrowser_trasa.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowser_trasa.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowser_trasa.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textBrowser_trasa.setObjectName("textBrowser_trasa")

        Window_map.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Window_map)
        self.statusbar.setObjectName("statusbar")
        Window_map.setStatusBar(self.statusbar)

        self.retranslateUi(Window_map)
        QtCore.QMetaObject.connectSlotsByName(Window_map)

        self.textBrowser_trasa.clear()
        self.wysw_opt(trasa_opt, koszt_trasy, adresy, dane_osob, adres_dom)

    # Przetłumaczenie interfejsu
    def retranslateUi(self, Window_map):
        _translate = QtCore.QCoreApplication.translate
        Window_map.setWindowTitle(_translate("Window_map", "Wyznaczona trasa"))

# Start okna
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window_map = QtWidgets.QMainWindow()
    ui = Ui_Window_map()
    ui.setupUi(Window_map)
    Window_map.show()
    sys.exit(app.exec_())
