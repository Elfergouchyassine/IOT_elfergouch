# Projet IoT – Capteur TempHumiX

Projet IoT réalisé à l'IMT Nord Europe (CERI Systèmes Numériques) : une chaîne complète de
relevé de **température et d'humidité**, du capteur jusqu'à l'interface utilisateur et la base
de données. Le capteur est identifié par le numéro de poste **42920**.

Le projet est découpé en **3 TP**, un par couche de l'architecture IoT.

## Architecture

```mermaid
flowchart LR
    subgraph TP1["TP1 – Objets (SIMULIDE/)"]
        S["Arduino UNO simulé<br/>DHT22 · LCD I2C · LED · bargraphe"]
    end

    subgraph TP2["TP2 – Réseau (RealSimulation/)"]
        A["Arduino UNO R4 WiFi<br/>capteur TempHumiX réel"]
        B[("Broker MQTT<br/>Mosquitto 192.168.1.1:1883")]
        A -- "publie TEMPERATURE / HUMIDITY / GET_DATE" --> B
        B -- "COMMAND / BARGRAPH / BLINK" --> A
    end

    subgraph TP3["TP3 – Application (IHM/)"]
        P["Client Python<br/>IHM PySide6"]
        D[("SQLite<br/>IOT.db")]
        C["Courbes<br/>Matplotlib"]
        P --> D --> C
    end

    S -. "même code, porté sur la vraie carte" .-> A
    B -- "souscrit aux mesures" --> P
    P -- "envoie les commandes" --> B
```

| TP | Couche | Ce qu'on y fait |
|----|--------|-----------------|
| **TP1** | Objets (capteurs / actionneurs) | Montages simulés sous SimulIDE, ajoutés un composant à la fois |
| **TP2** | Réseau | Wi-Fi, NTP et MQTT sur l'Arduino UNO R4, puis analyse des trames avec Wireshark |
| **TP3** | Application | Client MQTT Python, IHM PySide6, archivage SQLite et courbes |

## Organisation du dépôt

```
IOT_elfergouch/
├── SIMULIDE/              TP1 – un dossier par montage (.ino + .sim1)
│   ├── clignotement_led/    LED sur la broche 2
│   ├── bargraphe/           chenillard sur 10 LED
│   ├── capteur_dht22/       LED verte/rouge selon un seuil de température
│   ├── lcd_i2c/             « HELLO WORLD » sur LCD I2C
│   ├── lcd_i2c_dht22/       mesure affichée sur le LCD
│   └── TempHumiX/           capteur complet (dateur, LED de vie, port série)
│
├── RealSimulation/        TP2 – croquis Arduino UNO R4, dans l'ordre du TP
│   ├── TempAquisition/      passage de R3 à R4 (LCD Grove)
│   ├── Temp_RTC/            horloge RTC interne
│   ├── date_WIFI/           connexion Wi-Fi et synchro NTP
│   ├── ArduinoMQTTClient/   publication des mesures
│   ├── SouscriptionParams/  réception des commandes
│   └── OptimisationMQTT/    version finale : publie seulement si la valeur change
│
├── IHM/                   TP3 – programmes Python (PyCharm)
│   ├── console_mqtt_lecture/    client console qui lit les mesures
│   ├── console_mqtt_ecriture/   client console qui envoie les commandes
│   ├── console_mqtt_thread/     lecture et écriture réunies grâce à un thread
│   └── ihm_mqtt_simple/         IHM PySide6 + base SQLite + courbes (version finale)
│
├── interface_web/         Pour aller plus loin – la même IHM dans un navigateur (Node.js)
│
└── Compte Rendu_VF.pdf    compte rendu final des 3 TP
```

> Pour lancer l'IHM finale : `pip install paho-mqtt PySide6 matplotlib`, puis
> `python IHM/ihm_mqtt_simple/main.py`.

## Pour aller plus loin : l'interface web

`interface_web/` reprend l'IHM PySide6 dans un navigateur. Elle a trois onglets :
- **Tableau de bord** : connexion au broker, mesures en direct, commandes du capteur (NTP,
  start/stop, clignotements, bargraphe) ;
- **Courbes** : température et humidité entre deux dates ;
- **Base de données** : tableau des mesures archivées.

```
Navigateur (HTML + JS natif + Chart.js)
     │ REST            ▲ temps réel (Server-Sent Events)
     ▼                 │
Serveur Express ── client MQTT ──► Broker Mosquitto ◄──► Arduino UNO R4
     │
     ▼
SQLite (même table IOT_Data que l'IHM Python)
```

Lancement : `cd interface_web`, `npm install`, `npm start`, puis ouvrir http://localhost:3000.
Le détail (API, fichiers) est dans [interface_web/README.md](interface_web/README.md).

## Le rapport

Le compte rendu final est **`Compte Rendu_VF.pdf`**, à la racine du dépôt. Il suit les 3 TP, puis présente l'interface web.
Chaque partie commence par le lien avec le cours, puis montre les résultats (captures
SimulIDE, MQTTX, Wireshark, IHM) et répond aux questions de l'énoncé.

