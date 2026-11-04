import os
import sys

from PySide6.QtCore import Qt, QTimer, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QIntValidator, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit

from client_mqtt import ClientMQTT
from thread_mqtt import ThreadMQTT
from mon_ihm import Ui_MainWindow
from dialogue_courbe import CourbeDialog

# ---------------- Paramètres par défaut ----------------
id_pc = 42920
broker = '192.168.1.1'
port = 1883
username = 'mos_user'
password = 'mos_user'

topic_commande = f"/iot/COMMAND_{id_pc}"
topic_bargraphe = f"/iot/BARGRAPH_{id_pc}"
topic_periode = f"/iot/BLINK_{id_pc}"

CMD_SYNCHRO = 10
CMD_START = 20
CMD_STOP = 30
CMD_SLOW_BLINK = 40
CMD_FAST_BLINK = 50
CMD_CUSTOM_BLINK = 60


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)              # crée tous les widgets du fichier mon_ihm.py

        self.mqtt = None
        self.thread_mqtt = None
        self.debug = True

        # Image à gauche des paramètres du broker
        chemin_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "treepic.png")
        self.lblLogo.setPixmap(QPixmap(chemin_image).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio,
                                                            Qt.TransformationMode.SmoothTransformation))

        # Valeurs par défaut dans les champs
        self.lneIP.setText(broker)
        self.lnePort.setText(str(port))
        self.lneUser.setText(username)
        self.lnePassword.setText(password)
        self.lnePassword.setEchoMode(QLineEdit.EchoMode.Password)   # affiche ●●●●
        self.lneBlink.setText("500")

        # Validateurs : empêchent de taper n'importe quoi
        ip_regex = QRegularExpression(r"^(\d{1,3}\.){3}\d{1,3}$")
        self.lneIP.setValidator(QRegularExpressionValidator(ip_regex, self))
        self.lnePort.setValidator(QIntValidator(1, 65535, self))
        self.lneBlink.setValidator(QIntValidator(100, 10000, self))
        self.lneBargraph.setValidator(QIntValidator(0, 1023, self))

        # Timer d'affichage
        self.timer = QTimer()
        self.timer.timeout.connect(self.display)

        # Connexion signaux -> méthodes
        self.btnConnect.clicked.connect(self.connectMQTT)
        self.btnDisconnect.clicked.connect(self.disconnectMQTT)
        self.btnSynchroDateTime.clicked.connect(self.synchroDateTime)
        self.btnStartMeasure.clicked.connect(self.startMeasure)
        self.btnStopMeasure.clicked.connect(self.stopMeasure)
        self.btnFastBlink.clicked.connect(self.fastBlink)
        self.btnSlowBlink.clicked.connect(self.slowBlink)
        self.btnBlink.clicked.connect(self.customBlink)
        self.lneBargraph.returnPressed.connect(self.setBargraph)
        self.actionQuitter.triggered.connect(self.quit)
        self.actionCourbes.triggered.connect(self.afficherCourbes)

        self.set_connected(False)

    # Active / désactive les boutons selon l'état de la connexion
    def set_connected(self, connecte):
        self.btnConnect.setEnabled(not connecte)
        self.btnDisconnect.setEnabled(connecte)
        for w in (self.btnSynchroDateTime, self.btnStartMeasure, self.btnStopMeasure,
                  self.btnFastBlink, self.btnSlowBlink, self.btnBlink,
                  self.lneBlink, self.lneBargraph):
            w.setEnabled(connecte)

    # display : affiche les dernières valeurs (appelée par le timer)
    def display(self):
        self.lblDateTime.setText(self.mqtt.date_IdO)
        self.lblTemperature.setText(f"{self.mqtt.temperature} °C")
        self.lblHumidite.setText(f"{self.mqtt.humidite} %")

    # connectMQTT : lit les paramètres, se connecte, lance thread + timer
    def connectMQTT(self):
        try:
            self.mqtt = ClientMQTT(self.lneIP.text(), int(self.lnePort.text()),
                                   f"Client_IHM_{id_pc}",
                                   self.lneUser.text(), self.lnePassword.text())
            self.mqtt.connect_mqtt()
        except Exception as e:
            self.mqtt = None
            self.statusbar.showMessage(f"Erreur de connexion : {e}")
            return

        self.thread_mqtt = ThreadMQTT(self.mqtt)    # nouveau thread à chaque connexion
        self.thread_mqtt.start()
        self.timer.start(1000)                      # display() toutes les 1000 ms
        self.set_connected(True)
        self.statusbar.showMessage("Connection au broker MQTT OK")

    # disconnectMQTT : arrête timer, thread, puis la connexion
    def disconnectMQTT(self):
        self.timer.stop()
        if self.thread_mqtt is not None:
            self.thread_mqtt.stopthread()
            self.thread_mqtt.join()
            self.thread_mqtt = None
        if self.mqtt is not None:
            self.mqtt.disconnect_mqtt()
            self.mqtt = None
        self.set_connected(False)
        self.statusbar.showMessage("Déconnecté du broker MQTT")

    # Envoi d'une commande (utilisé par tous les boutons)
    def send_command(self, code, texte):
        if self.mqtt is None:
            self.statusbar.showMessage("Non connecté au broker")
            return
        self.mqtt.publish_mqtt(topic_commande, code)
        self.statusbar.showMessage(texte)

    def synchroDateTime(self):
        self.send_command(CMD_SYNCHRO, "Synchronisation NTP demandée")

    def startMeasure(self):
        self.send_command(CMD_START, "Démarrage des mesures")
        self.send_command(CMD_FAST_BLINK, "Mesures démarrées (clignotement rapide)")

    def stopMeasure(self):
        self.send_command(CMD_STOP, "Arrêt des mesures")
        self.send_command(CMD_SLOW_BLINK, "Mesures arrêtées (clignotement lent)")

    def fastBlink(self):
        self.send_command(CMD_FAST_BLINK, "Clignotement rapide")

    def slowBlink(self):
        self.send_command(CMD_SLOW_BLINK, "Clignotement lent")

    # customBlink : lit la période puis envoie BLINK + commande 60
    def customBlink(self):
        texte = self.lneBlink.text()
        if not texte.isdigit() or int(texte) % 100 != 0:
            self.statusbar.showMessage("Période invalide : multiple de 100 ms attendu")
            return
        self.mqtt.publish_mqtt(topic_periode, int(texte))
        self.send_command(CMD_CUSTOM_BLINK, f"Clignotement personnalisé : {texte} ms")

    # setBargraph : appelée quand on appuie sur Entrée dans le champ
    def setBargraph(self):
        texte = self.lneBargraph.text()
        if not texte.isdigit():
            return
        self.mqtt.publish_mqtt(topic_bargraphe, int(texte))
        self.statusbar.showMessage(f"Bargraphe : {texte}")

    # afficherCourbes : ouvre la boîte de dialogue des courbes (section 6.4)
    def afficherCourbes(self):
        dialogue = CourbeDialog()
        dialogue.exec()

    # quit : quitter proprement (menu Fichier > Quitter)
    def quit(self):
        self.close()                 # déclenche closeEvent ci-dessous

    def closeEvent(self, event):
        # appelée aussi quand on clique sur la croix X
        if self.mqtt is not None:
            self.disconnectMQTT()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())