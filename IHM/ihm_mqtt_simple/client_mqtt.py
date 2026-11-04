import sqlite3
from datetime import datetime

from paho.mqtt import client as mqtt_client


class ClientMQTT:
    def __init__(self, ip_address, port, client_id, username, password):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = None

        # Dernières valeurs reçues du capteur
        self.id_capteur = 0
        self.version = "?"
        self.temperature = "?"
        self.humidite = "?"
        self.date_IdO = "?"

        # Base SQLite (section 5)
        self.conn = None
        self.tablename = None

    # ------------------------------------------------------------------
    # Section 5 a) : connexion à la base SQLite
    # ------------------------------------------------------------------
    def connect_sqlite(self, database_name="IOT.db", table_name="IOT_Data"):
        self.tablename = table_name
        self.conn = sqlite3.connect(database_name)    # crée le fichier s'il n'existe pas
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {self.tablename} "
                          "(Id_capteur integer, Date text, Version text, "
                          "Temperature real, Humidite real)")
        self.conn.commit()
        print(f"Base SQLite ouverte : {database_name} / table {self.tablename}")

    # ------------------------------------------------------------------
    # Section 5 b) : déconnexion de la base SQLite
    # ------------------------------------------------------------------
    def disconnect_sqlite(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print("Base SQLite fermée")

    # ------------------------------------------------------------------
    # Enregistre une ligne dans la base
    # ------------------------------------------------------------------
    def save_sqlite(self):
        if self.conn is None:
            return
        try:
            # "02/11/2026 15:59:57" -> "2026-11-02 15:59:57" (format triable)
            date_iso = datetime.strptime(self.date_IdO, "%d/%m/%Y %H:%M:%S") \
                               .strftime("%Y-%m-%d %H:%M:%S")
            self.conn.execute(f"INSERT INTO {self.tablename} VALUES (?,?,?,?,?)",
                              (self.id_capteur, date_iso, self.version,
                               float(self.temperature), float(self.humidite)))
            self.conn.commit()
            print(f"Archivé : {self.id_capteur} {date_iso} "
                  f"{self.temperature} °C {self.humidite} %")
        except ValueError:
            # une valeur vaut encore "?" ou la date est mal formée : on n'archive pas
            pass

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print(f"Connecté au broker MQTT : {self.ip_address} {self.port}")
            else:
                print(f"Échec de connexion au broker, code retour : {rc}")

        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2,
                                         self.client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.connect(self.ip_address, self.port)
        return self.client

    def disconnect_mqtt(self) -> None:
        if self.client is not None:
            self.client.disconnect()
            print("Déconnecté du broker MQTT")

    def publish_mqtt(self, topic, message, qos=0):
        result = self.client.publish(topic, message, qos)
        if result.rc == mqtt_client.MQTT_ERR_SUCCESS:
            print(f"Publication : `{message}` sur `{topic}`")
        else:
            print(f"Échec de publication sur `{topic}`")

    # ------------------------------------------------------------------
    # Section 5 d) : souscription + archivage au dernier topic publié
    # ------------------------------------------------------------------
    def subscribe_mqtt(self, topic, qos=0):
        def on_message(client, userdata, msg):
            valeur = msg.payload.decode()
            self.id_capteur = int(msg.topic[-5:])     # "/iot/..._42921" -> 42921
            if "VERSION_" in msg.topic:
                self.version = valeur
            elif "TEMPERATURE_" in msg.topic:
                self.temperature = valeur
            elif "HUMIDITY_" in msg.topic:
                self.humidite = valeur
            elif "GET_DATE_" in msg.topic:
                self.date_IdO = valeur
                # GET_DATE est le DERNIER topic publié par l'Arduino :
                # température et humidité sont donc à jour -> on archive
                self.save_sqlite()

        self.client.subscribe(topic, qos)
        self.client.on_message = on_message

    def wait_mqtt(self, timeout=0):
        if timeout == 0:
            self.client.loop_forever()
        else:
            self.client.loop(timeout=timeout)