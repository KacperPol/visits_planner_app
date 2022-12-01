from PyQt5 import QtCore, QtGui, QtWidgets
from okno_mapa import Ui_Window_map
import algorytm_komi as Alg

global max_klientow, base_max_klientow, adresy, ID_punktow, dane_osob, label, adres_dom
max_klientow = 5
base_max_klientow = 5
adresy=[]
ID_punktow=[]
dane_osob=[]
label=[]

class Ui_Window_main(object):

    # Wyznaczenie optymalnej drogi (start algorytmu)
    def start_aplikacji(self):
        global ID_punktow, adresy, dane_osob
        for i in range(0, len(ID_punktow)):
            ID_punktow[i] = int(ID_punktow[i])
        self.dodaj_adres_dom()
        URL_image, trasa_opt, koszt_trasy = Alg.wyznacz_trase(ID_punktow)
        #print(URL_image)
        self.OpenWindow_map(URL_image, trasa_opt, koszt_trasy, adresy, dane_osob, adres_dom)
        self.czysc_wszystko()

    # Wczytanie całej bazy klientów
    def wczytaj_baze(self):
        global adresy, dane_osob, label, adres_dom
        adresy, dane_osob = Alg.czytaj_baze()
        self.listWidget.clear()
        adres_dom = str(adresy[0])
        dane_osob.pop(0)
        adresy.pop(0)
        for i in range(len(adresy)):
            label.append(str(dane_osob[i]) + ", " + str(adresy[i]))
        self.listWidget.addItems(label)

    # Wybranie klientów po indeksach
    def dodaj_klientow(self):
        global max_klientow, label, ID_punktow
        if max_klientow > 0:
            self.textBrowser_wybrani.append(str(self.listWidget.currentItem().text()))
            ID_punktow_temp = self.listWidget.currentItem().text()
            ID_punktow.append(label.index(str(ID_punktow_temp)))
            max_klientow = max_klientow - 1
        self.lineEdit_Lklientow.setText(str(max_klientow))
        #self.wysw_wybr()

    # Czyszczenie zmiennych
    def czysc_wszystko(self):
        global max_klientow, ID_punktow, base_max_klientow
        max_klientow = base_max_klientow
        ID_punktow = []
        self.textBrowser_wybrani.clear()
        self.lineEdit_Lklientow.setText(str(max_klientow))

    # Odczytanie wybranego indeksu numeru domowego z GUI
    def dodaj_adres_dom(self):
        global ID_punktow
        ID_punktow.insert(0,0)
        #print("wybrano adres domowy: " + str(self.spinBox_dom.value()))
        #print(type(self.spinBox_dom.value()))

    # Otwieranie nowego okna z mapą
    def OpenWindow_map(self,URL_image, trasa_opt, koszt_trasy, adresy, dane_osob, adres_dom):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Window_map()
        self.ui.setupUi(self.window,URL_image, trasa_opt, koszt_trasy, adresy, dane_osob, adres_dom)
        self.window.show()

    def setupUi(self, Window_main):
        Window_main.setObjectName("Window_main")
        Window_main.resize(621, 756)
        font = QtGui.QFont()
        font.setPointSize(10)
        Window_main.setFont(font)
        Window_main.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(Window_main)
        self.centralwidget.setObjectName("centralwidget")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 370, 601, 351))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")

        self.pushButton_startALG = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.start_aplikacji())
        self.pushButton_startALG.setGeometry(QtCore.QRect(10, 300, 581, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_startALG.setFont(font)
        self.pushButton_startALG.setObjectName("pushButton_startALG")

        self.textBrowser_wybrani = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_wybrani.setGeometry(QtCore.QRect(10, 30, 581, 211))
        self.textBrowser_wybrani.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowser_wybrani.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowser_wybrani.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textBrowser_wybrani.setObjectName("textBrowser_wybrani")

        self.pushButton_usunID = QtWidgets.QPushButton(self.groupBox, clicked = lambda: self.czysc_wszystko())
        self.pushButton_usunID.setGeometry(QtCore.QRect(10, 250, 581, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_usunID.setFont(font)
        self.pushButton_usunID.setObjectName("pushButton_usunID")

        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 10, 601, 351))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")

        self.listWidget = QtWidgets.QListWidget(self.groupBox_4, clicked = lambda: self.dodaj_klientow())
        self.listWidget.setGeometry(QtCore.QRect(10, 70, 581, 271))
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.listWidget.setObjectName("listWidget")

        self.label_max_klientow = QtWidgets.QLabel(self.groupBox_4)
        self.label_max_klientow.setGeometry(QtCore.QRect(10, 30, 451, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_max_klientow.setFont(font)
        self.label_max_klientow.setObjectName("label_max_klientow")

        self.lineEdit_Lklientow = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_Lklientow.setGeometry(QtCore.QRect(460, 30, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_Lklientow.setFont(font)
        self.lineEdit_Lklientow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_Lklientow.setText(str(max_klientow))
        self.lineEdit_Lklientow.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_Lklientow.setReadOnly(True)
        self.lineEdit_Lklientow.setObjectName("lineEdit_Lklientow")

        Window_main.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Window_main)
        self.statusbar.setObjectName("statusbar")
        Window_main.setStatusBar(self.statusbar)

        self.retranslateUi(Window_main)
        QtCore.QMetaObject.connectSlotsByName(Window_main)

        # Wczytanie bazy po inicjalizacji okna
        self.wczytaj_baze()

    def retranslateUi(self, Window_main):
        _translate = QtCore.QCoreApplication.translate
        Window_main.setWindowTitle(_translate("Window_main", "MainWindow"))
        self.groupBox.setTitle(_translate("Window_main", "Wyznaczeni klienci"))
        self.pushButton_startALG.setText(_translate("Window_main", "Wyznacz kolejność wizyt"))
        self.pushButton_usunID.setText(_translate("Window_main", "Wyczyść"))
        self.groupBox_4.setTitle(_translate("Window_main", "Baza klientów"))
        self.label_max_klientow.setText(_translate("Window_main", "Do dziennego limitu można dodać jeszcze klientów:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window_main = QtWidgets.QMainWindow()
    ui = Ui_Window_main()
    ui.setupUi(Window_main)
    Window_main.show()
    sys.exit(app.exec_())
