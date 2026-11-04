const EventEmitter = require('events');
const mqtt = require('mqtt');

// Équivalent JavaScript de la classe ClientMQTT + ThreadMQTT de l'IHM Python.
// Émet 'mesure' à chaque nouvelle valeur et 'etat' quand la connexion change.
class ClientMQTT extends EventEmitter {
  constructor(base) {
    super();
    this.base = base;
    this.client = null;
    this.idCapteur = null;
    this.connecte = false;
    this.derniere = { version: '?', temperature: '?', humidite: '?', date: '?' };
  }

  topics(id) {
    return {
      version: `/iot/VERSION_${id}`,
      temperature: `/iot/TEMPERATURE_${id}`,
      humidite: `/iot/HUMIDITY_${id}`,
      date: `/iot/GET_DATE_${id}`,
      commande: `/iot/COMMAND_${id}`,
      bargraphe: `/iot/BARGRAPH_${id}`,
      blink: `/iot/BLINK_${id}`,
    };
  }

  connecter({ host, port, username, password, idCapteur }) {
    this.deconnecter();
    this.idCapteur = Number(idCapteur);
    const t = this.topics(this.idCapteur);

    return new Promise((resolve, reject) => {
      // Id différent du client Python pour pouvoir lancer les deux en même temps
      this.client = mqtt.connect(`mqtt://${host}:${port}`, {
        clientId: `Client_W${this.idCapteur}`,
        username,
        password,
        connectTimeout: 5000,
        reconnectPeriod: 0,
      });

      this.client.once('connect', () => {
        this.connecte = true;
        this.client.subscribe([t.version, t.temperature, t.humidite, t.date]);
        console.log(`Connecté au broker MQTT : ${host} ${port}`);
        this.emit('etat', this.etat());
        resolve();
      });

      this.client.once('error', (err) => {
        this.deconnecter();
        reject(err);
      });

      this.client.on('close', () => {
        if (this.connecte) {
          this.connecte = false;
          this.emit('etat', this.etat());
        }
      });

      this.client.on('message', (topic, payload) => this.reception(topic, payload.toString()));
    });
  }

  reception(topic, valeur) {
    if (topic.includes('VERSION_')) this.derniere.version = valeur;
    else if (topic.includes('TEMPERATURE_')) this.derniere.temperature = valeur;
    else if (topic.includes('HUMIDITY_')) this.derniere.humidite = valeur;
    else if (topic.includes('GET_DATE_')) {
      this.derniere.date = valeur;
      // GET_DATE est le dernier topic publié par l'Arduino : la mesure est complète
      this.base.enregistrer({ idCapteur: this.idCapteur, ...this.derniere });
    }
    this.emit('mesure', this.derniere);
  }

  publier(cle, message) {
    if (!this.connecte) throw new Error('Non connecté au broker');
    const topic = this.topics(this.idCapteur)[cle];
    this.client.publish(topic, String(message));
    console.log(`Publication : \`${message}\` sur \`${topic}\``);
  }

  deconnecter() {
    if (this.client) {
      this.client.removeAllListeners();
      this.client.end(true);
      this.client = null;
    }
    if (this.connecte) {
      this.connecte = false;
      this.emit('etat', this.etat());
    }
  }

  etat() {
    return { connecte: this.connecte, idCapteur: this.idCapteur, ...this.derniere };
  }
}

module.exports = ClientMQTT;
