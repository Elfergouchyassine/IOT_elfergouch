# Interface web – Capteur TempHumiX

Version web de l'IHM PySide6 (`IHM/ihm_mqtt_simple`) : affichage en direct, commandes du
capteur, consultation de la base et courbes, depuis un navigateur.

```
Navigateur (HTML + JS natif + Chart.js)
      │  REST (fetch)   ▲ temps réel (Server-Sent Events)
      ▼                 │
Serveur Express (server.js) ── client MQTT ──► Broker Mosquitto ◄──► Arduino UNO R4
      │
      ▼
SQLite (data/IOT.db, même table IOT_Data que l'IHM Python)
```

## Lancer

```bash
cd interface_web
npm install
npm start          # http://localhost:3000
```

Le PC doit être sur le réseau Wi-Fi IoT pour joindre le broker `192.168.1.1:1883`.
Les valeurs par défaut se règlent dans `src/config.js`.

## Fonctions

| Onglet | Contenu |
|--------|---------|
| Tableau de bord | Connexion au broker, date/température/humidité en direct, commandes (NTP, start/stop, clignotements, bargraphe) |
| Courbes | Température et humidité entre deux dates, filtrées par capteur |
| Base de données | Tableau des mesures archivées |

## Organisation

| Fichier | Rôle |
|---------|------|
| `server.js` | Routes Express (API REST + flux SSE) |
| `src/clientMqtt.js` | Connexion MQTT, souscription aux 4 topics, publication des commandes |
| `src/database.js` | Archivage SQLite et requêtes |
| `src/config.js` | Paramètres par défaut (broker, id capteur, codes commande) |
| `public/` | Interface : `index.html`, `style.css`, `app.js` |

## API

| Méthode | Route | Rôle |
|---------|-------|------|
| GET | `/api/events` | Flux temps réel des dernières valeurs |
| POST | `/api/connect` · `/api/disconnect` | Connexion au broker |
| POST | `/api/command/:action` | `synchro`, `start`, `stop`, `slowBlink`, `fastBlink` |
| POST | `/api/blink` | `{ "periode": 500 }` puis commande 60 |
| POST | `/api/bargraph` | `{ "valeur": 512 }` |
| GET | `/api/mesures?debut=&fin=&capteur=` | Mesures archivées |
| GET | `/api/capteurs` | Liste des capteurs présents en base |
