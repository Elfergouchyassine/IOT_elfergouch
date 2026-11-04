import os
from threading import Thread

id_pc = 42920

topic_version = f"/iot/VERSION_{id_pc}"
topic_temperature = f"/iot/TEMPERATURE_{id_pc}"
topic_humidite = f"/iot/HUMIDITY_{id_pc}"
topic_datetime = f"/iot/GET_DATE_{id_pc}"

# Base SQLite toujours à côté de ce fichier (peu importe d'où on lance le programme)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IOT.db")
TABLE_NAME = "IOT_Data"


class ThreadMQTT(Thread):
    def __init__(self, client_mqtt):
        Thread.__init__(self)
        self.mqtt = client_mqtt
        self.stop = False
        self.daemon = True

    def run(self):
        # Section 5 c) : la base est ouverte DANS le thread qui l'utilise
        self.mqtt.connect_sqlite(DB_PATH, TABLE_NAME)

        self.mqtt.subscribe_mqtt(topic_version)
        self.mqtt.subscribe_mqtt(topic_temperature)
        self.mqtt.subscribe_mqtt(topic_humidite)
        self.mqtt.subscribe_mqtt(topic_datetime)

        while not self.stop:
            self.mqtt.wait_mqtt(timeout=1.0)

        self.mqtt.disconnect_sqlite()

    def stopthread(self):
        self.stop = True