# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'graphe.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDateTimeEdit, QDialog,
    QDialogButtonBox, QGraphicsView, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_GraphWindow(object):
    def setupUi(self, GraphWindow):
        if not GraphWindow.objectName():
            GraphWindow.setObjectName(u"GraphWindow")
        GraphWindow.resize(640, 560)
        self.verticalLayout = QVBoxLayout(GraphWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gbIntervalle = QGroupBox(GraphWindow)
        self.gbIntervalle.setObjectName(u"gbIntervalle")
        self.gridIntervalle = QGridLayout(self.gbIntervalle)
        self.gridIntervalle.setObjectName(u"gridIntervalle")
        self.labelDebut = QLabel(self.gbIntervalle)
        self.labelDebut.setObjectName(u"labelDebut")

        self.gridIntervalle.addWidget(self.labelDebut, 0, 0, 1, 1)

        self.dteStartTime = QDateTimeEdit(self.gbIntervalle)
        self.dteStartTime.setObjectName(u"dteStartTime")
        self.dteStartTime.setCalendarPopup(True)

        self.gridIntervalle.addWidget(self.dteStartTime, 0, 1, 1, 1)

        self.labelFin = QLabel(self.gbIntervalle)
        self.labelFin.setObjectName(u"labelFin")

        self.gridIntervalle.addWidget(self.labelFin, 1, 0, 1, 1)

        self.dteEndTime = QDateTimeEdit(self.gbIntervalle)
        self.dteEndTime.setObjectName(u"dteEndTime")
        self.dteEndTime.setCalendarPopup(True)

        self.gridIntervalle.addWidget(self.dteEndTime, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.gbIntervalle)

        self.graphicsView = QGraphicsView(GraphWindow)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)

        self.layoutBoutons = QHBoxLayout()
        self.layoutBoutons.setObjectName(u"layoutBoutons")
        self.btnClearData = QPushButton(GraphWindow)
        self.btnClearData.setObjectName(u"btnClearData")

        self.layoutBoutons.addWidget(self.btnClearData)

        self.btnLoadData = QPushButton(GraphWindow)
        self.btnLoadData.setObjectName(u"btnLoadData")

        self.layoutBoutons.addWidget(self.btnLoadData)

        self.buttonBox = QDialogButtonBox(GraphWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.layoutBoutons.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.layoutBoutons)


        self.retranslateUi(GraphWindow)
        self.buttonBox.accepted.connect(GraphWindow.accept)
        self.buttonBox.rejected.connect(GraphWindow.reject)

        QMetaObject.connectSlotsByName(GraphWindow)
    # setupUi

    def retranslateUi(self, GraphWindow):
        GraphWindow.setWindowTitle(QCoreApplication.translate("GraphWindow", u"Graphique des donn\u00e9es de temp\u00e9rature et d'humidit\u00e9", None))
        self.gbIntervalle.setTitle(QCoreApplication.translate("GraphWindow", u"Param\u00e8tres de l'intervalle temporel", None))
        self.labelDebut.setText(QCoreApplication.translate("GraphWindow", u"Date et heure de d\u00e9but", None))
        self.dteStartTime.setDisplayFormat(QCoreApplication.translate("GraphWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.labelFin.setText(QCoreApplication.translate("GraphWindow", u"Date et heure de fin", None))
        self.dteEndTime.setDisplayFormat(QCoreApplication.translate("GraphWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.btnClearData.setText(QCoreApplication.translate("GraphWindow", u"Effacer les courbes", None))
        self.btnLoadData.setText(QCoreApplication.translate("GraphWindow", u"Charger les donn\u00e9es", None))
    # retranslateUi

