import os
import sqlite3
from datetime import datetime

from PySide6.QtCore import QDateTime
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QDialog, QGraphicsPixmapItem
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from graphe import Ui_GraphWindow

id_pc = 42920

# même base que celle remplie par thread_mqtt.py
database_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IOT.db")
table_name = 'IOT_Data'


class CourbeDialog(QDialog, Ui_GraphWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Intervalle par défaut : la dernière heure
        dte = QDateTime.currentDateTime()
        dts = dte.addSecs(-3600)
        self.dteStartTime.setDateTime(dts)
        self.dteEndTime.setDateTime(dte)

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.btnLoadData.clicked.connect(self.afficher_courbe)
        self.btnClearData.clicked.connect(self.effacer_courbe)

    # Convertit une figure matplotlib en image Qt
    def figure_to_pixmap(self, fig):
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()
        width, height = int(width), int(height)
        buf = canvas.buffer_rgba()
        image = QImage(buf, width, height, QImage.Format.Format_RGBA8888)
        return QPixmap.fromImage(image)

    def afficher_courbe(self):
        # format "yyyy-MM-dd HH:mm:ss" = même format que dans la base
        debut = self.dteStartTime.text()
        fin = self.dteEndTime.text()

        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cur.execute(f"SELECT Date, Temperature, Humidite FROM {table_name} "
                    "WHERE Date BETWEEN ? AND ? ORDER BY Date ASC", (debut, fin))
        rows = cur.fetchall()
        conn.close()

        if len(rows) == 0:
            self.setWindowTitle("Aucune donnée dans cet intervalle")
            return
        self.setWindowTitle(f"{len(rows)} mesures de {debut} à {fin}")

        date_x = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in rows]
        temp_y = [r[1] for r in rows]
        humi_y = [r[2] for r in rows]

        self.scene.clear()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(date_x, temp_y, marker="o", label="Température (°C)")
        ax.plot(date_x, humi_y, marker="+", label="Humidité (%)")
        ax.set_title(f"Données capteur IdO {id_pc}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Valeurs")
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()          # incline les dates pour qu'elles soient lisibles

        pixmap = self.figure_to_pixmap(fig)
        plt.close(fig)               # libère la mémoire de la figure

        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def effacer_courbe(self):
        self.scene.clear()
