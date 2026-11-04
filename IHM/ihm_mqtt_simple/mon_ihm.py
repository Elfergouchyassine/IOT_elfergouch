# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mon_ihm.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 600)
        self.actionCourbes = QAction(MainWindow)
        self.actionCourbes.setObjectName(u"actionCourbes")
        self.actionQuitter = QAction(MainWindow)
        self.actionQuitter.setObjectName(u"actionQuitter")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gbBroker = QGroupBox(self.centralwidget)
        self.gbBroker.setObjectName(u"gbBroker")
        self.gridBroker = QGridLayout(self.gbBroker)
        self.gridBroker.setObjectName(u"gridBroker")
        self.lblLogo = QLabel(self.gbBroker)
        self.lblLogo.setObjectName(u"lblLogo")
        self.lblLogo.setMinimumSize(QSize(150, 150))
        self.lblLogo.setAlignment(Qt.AlignCenter)

        self.gridBroker.addWidget(self.lblLogo, 0, 0, 4, 1)

        self.labelIP = QLabel(self.gbBroker)
        self.labelIP.setObjectName(u"labelIP")
        self.labelIP.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridBroker.addWidget(self.labelIP, 0, 1, 1, 1)

        self.lneIP = QLineEdit(self.gbBroker)
        self.lneIP.setObjectName(u"lneIP")

        self.gridBroker.addWidget(self.lneIP, 0, 2, 1, 1)

        self.labelPort = QLabel(self.gbBroker)
        self.labelPort.setObjectName(u"labelPort")
        self.labelPort.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridBroker.addWidget(self.labelPort, 1, 1, 1, 1)

        self.lnePort = QLineEdit(self.gbBroker)
        self.lnePort.setObjectName(u"lnePort")

        self.gridBroker.addWidget(self.lnePort, 1, 2, 1, 1)

        self.labelUser = QLabel(self.gbBroker)
        self.labelUser.setObjectName(u"labelUser")
        self.labelUser.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridBroker.addWidget(self.labelUser, 2, 1, 1, 1)

        self.lneUser = QLineEdit(self.gbBroker)
        self.lneUser.setObjectName(u"lneUser")

        self.gridBroker.addWidget(self.lneUser, 2, 2, 1, 1)

        self.labelPassword = QLabel(self.gbBroker)
        self.labelPassword.setObjectName(u"labelPassword")
        self.labelPassword.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridBroker.addWidget(self.labelPassword, 3, 1, 1, 1)

        self.lnePassword = QLineEdit(self.gbBroker)
        self.lnePassword.setObjectName(u"lnePassword")

        self.gridBroker.addWidget(self.lnePassword, 3, 2, 1, 1)

        self.btnConnect = QPushButton(self.gbBroker)
        self.btnConnect.setObjectName(u"btnConnect")
        self.btnConnect.setMinimumSize(QSize(0, 40))

        self.gridBroker.addWidget(self.btnConnect, 4, 1, 1, 1)

        self.btnDisconnect = QPushButton(self.gbBroker)
        self.btnDisconnect.setObjectName(u"btnDisconnect")
        self.btnDisconnect.setMinimumSize(QSize(0, 40))

        self.gridBroker.addWidget(self.btnDisconnect, 4, 2, 1, 1)


        self.verticalLayout.addWidget(self.gbBroker)

        self.gbDonnees = QGroupBox(self.centralwidget)
        self.gbDonnees.setObjectName(u"gbDonnees")
        self.gridDonnees = QGridLayout(self.gbDonnees)
        self.gridDonnees.setObjectName(u"gridDonnees")
        self.lblDateTime = QLabel(self.gbDonnees)
        self.lblDateTime.setObjectName(u"lblDateTime")
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(14)
        self.lblDateTime.setFont(font)
        self.lblDateTime.setAlignment(Qt.AlignCenter)

        self.gridDonnees.addWidget(self.lblDateTime, 0, 0, 1, 4)

        self.labelTemperature = QLabel(self.gbDonnees)
        self.labelTemperature.setObjectName(u"labelTemperature")

        self.gridDonnees.addWidget(self.labelTemperature, 1, 0, 1, 1)

        self.lblTemperature = QLabel(self.gbDonnees)
        self.lblTemperature.setObjectName(u"lblTemperature")
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(12)
        self.lblTemperature.setFont(font1)

        self.gridDonnees.addWidget(self.lblTemperature, 1, 1, 1, 1)

        self.labelHumidite = QLabel(self.gbDonnees)
        self.labelHumidite.setObjectName(u"labelHumidite")

        self.gridDonnees.addWidget(self.labelHumidite, 1, 2, 1, 1)

        self.lblHumidite = QLabel(self.gbDonnees)
        self.lblHumidite.setObjectName(u"lblHumidite")
        self.lblHumidite.setFont(font1)

        self.gridDonnees.addWidget(self.lblHumidite, 1, 3, 1, 1)


        self.verticalLayout.addWidget(self.gbDonnees)

        self.gbCommandes = QGroupBox(self.centralwidget)
        self.gbCommandes.setObjectName(u"gbCommandes")
        self.gridCommandes = QGridLayout(self.gbCommandes)
        self.gridCommandes.setObjectName(u"gridCommandes")
        self.btnSynchroDateTime = QPushButton(self.gbCommandes)
        self.btnSynchroDateTime.setObjectName(u"btnSynchroDateTime")
        self.btnSynchroDateTime.setMinimumSize(QSize(0, 40))

        self.gridCommandes.addWidget(self.btnSynchroDateTime, 0, 0, 1, 2)

        self.btnStopMeasure = QPushButton(self.gbCommandes)
        self.btnStopMeasure.setObjectName(u"btnStopMeasure")
        self.btnStopMeasure.setMinimumSize(QSize(0, 40))

        self.gridCommandes.addWidget(self.btnStopMeasure, 1, 0, 1, 1)

        self.btnStartMeasure = QPushButton(self.gbCommandes)
        self.btnStartMeasure.setObjectName(u"btnStartMeasure")
        self.btnStartMeasure.setMinimumSize(QSize(0, 40))

        self.gridCommandes.addWidget(self.btnStartMeasure, 1, 1, 1, 1)

        self.btnSlowBlink = QPushButton(self.gbCommandes)
        self.btnSlowBlink.setObjectName(u"btnSlowBlink")
        self.btnSlowBlink.setMinimumSize(QSize(0, 40))

        self.gridCommandes.addWidget(self.btnSlowBlink, 2, 0, 1, 1)

        self.btnFastBlink = QPushButton(self.gbCommandes)
        self.btnFastBlink.setObjectName(u"btnFastBlink")
        self.btnFastBlink.setMinimumSize(QSize(0, 40))

        self.gridCommandes.addWidget(self.btnFastBlink, 2, 1, 1, 1)

        self.btnBlink = QPushButton(self.gbCommandes)
        self.btnBlink.setObjectName(u"btnBlink")
        self.btnBlink.setMinimumSize(QSize(0, 40))

        self.gridCommandes.addWidget(self.btnBlink, 3, 0, 1, 1)

        self.lneBlink = QLineEdit(self.gbCommandes)
        self.lneBlink.setObjectName(u"lneBlink")
        self.lneBlink.setAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.gridCommandes.addWidget(self.lneBlink, 3, 1, 1, 1)

        self.labelBargraph = QLabel(self.gbCommandes)
        self.labelBargraph.setObjectName(u"labelBargraph")

        self.gridCommandes.addWidget(self.labelBargraph, 4, 0, 1, 1)

        self.lneBargraph = QLineEdit(self.gbCommandes)
        self.lneBargraph.setObjectName(u"lneBargraph")

        self.gridCommandes.addWidget(self.lneBargraph, 4, 1, 1, 1)


        self.verticalLayout.addWidget(self.gbCommandes)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 480, 22))
        self.menuFichier = QMenu(self.menubar)
        self.menuFichier.setObjectName(u"menuFichier")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menuFichier.addAction(self.actionCourbes)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionQuitter)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mon capteur IDO via MQTT (c)2026 CERI SN - PPI", None))
        self.actionCourbes.setText(QCoreApplication.translate("MainWindow", u"Afficher les courbes", None))
        self.actionQuitter.setText(QCoreApplication.translate("MainWindow", u"Quitter", None))
        self.gbBroker.setTitle(QCoreApplication.translate("MainWindow", u"Param\u00e8tres de communication du Broker MQTT", None))
        self.labelIP.setText(QCoreApplication.translate("MainWindow", u"Adresse IP :", None))
        self.labelPort.setText(QCoreApplication.translate("MainWindow", u"Port :", None))
        self.labelUser.setText(QCoreApplication.translate("MainWindow", u"Utilisateur :", None))
        self.labelPassword.setText(QCoreApplication.translate("MainWindow", u"Mot de passe :", None))
        self.btnConnect.setText(QCoreApplication.translate("MainWindow", u"Connecter", None))
        self.btnDisconnect.setText(QCoreApplication.translate("MainWindow", u"D\u00e9connecter", None))
        self.gbDonnees.setTitle(QCoreApplication.translate("MainWindow", u"Affichage des donn\u00e9es du capteur", None))
        self.lblDateTime.setText(QCoreApplication.translate("MainWindow", u"00/00/0000 00:00:00", None))
        self.labelTemperature.setText(QCoreApplication.translate("MainWindow", u"<b>Temp\u00e9rature (en \u00b0C) :</b>", None))
        self.lblTemperature.setText(QCoreApplication.translate("MainWindow", u"00.0", None))
        self.labelHumidite.setText(QCoreApplication.translate("MainWindow", u"<b>Humidit\u00e9 (en %) :</b>", None))
        self.lblHumidite.setText(QCoreApplication.translate("MainWindow", u"00.0", None))
        self.gbCommandes.setTitle(QCoreApplication.translate("MainWindow", u"Commandes", None))
        self.btnSynchroDateTime.setText(QCoreApplication.translate("MainWindow", u"Synchronisation de la date et heure du capteur (NTP)", None))
        self.btnStopMeasure.setText(QCoreApplication.translate("MainWindow", u"Arr\u00eater les mesures", None))
        self.btnStartMeasure.setText(QCoreApplication.translate("MainWindow", u"D\u00e9marrer les mesures", None))
        self.btnSlowBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement lent", None))
        self.btnFastBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement rapide", None))
        self.btnBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement personnalis\u00e9 (ms)", None))
        self.labelBargraph.setText(QCoreApplication.translate("MainWindow", u"Valeur du bargraphe (Entr\u00e9e pour envoyer) :", None))
        self.menuFichier.setTitle(QCoreApplication.translate("MainWindow", u"Fichier", None))
    # retranslateUi

