const path = require('path');
const express = require('express');

const config = require('./src/config');
const BaseIoT = require('./src/database');
const ClientMQTT = require('./src/clientMqtt');

const base = new BaseIoT(config.database, config.table);
const mqtt = new ClientMQTT(base);
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/lib', express.static(path.join(__dirname, 'node_modules', 'chart.js', 'dist')));

// ---------------- Temps réel (Server-Sent Events) ----------------
const abonnes = new Set();

function diffuser(evenement, donnees) {
  const msg = `event: ${evenement}\ndata: ${JSON.stringify(donnees)}\n\n`;
  abonnes.forEach((res) => res.write(msg));
}

mqtt.on('mesure', () => diffuser('etat', mqtt.etat()));
mqtt.on('etat', (etat) => diffuser('etat', etat));

app.get('/api/events', (req, res) => {
  res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
  res.flushHeaders();
  res.write(`event: etat\ndata: ${JSON.stringify(mqtt.etat())}\n\n`);
  abonnes.add(res);
  res.on('close', () => abonnes.delete(res));
});

// ---------------- Connexion au broker ----------------
app.get('/api/config', (req, res) => {
  res.json({ ...config.mqtt, idCapteur: config.idCapteur });
});

app.get('/api/etat', (req, res) => res.json(mqtt.etat()));

app.post('/api/connect', async (req, res) => {
  const params = { ...config.mqtt, idCapteur: config.idCapteur, ...req.body };
  try {
    await mqtt.connecter(params);
    res.json(mqtt.etat());
  } catch (err) {
    res.status(502).json({ erreur: `Connexion impossible : ${err.message}` });
  }
});

app.post('/api/disconnect', (req, res) => {
  mqtt.deconnecter();
  res.json(mqtt.etat());
});

// ---------------- Commandes vers le capteur ----------------
function publier(res, cle, valeur, texte) {
  try {
    mqtt.publier(cle, valeur);
    res.json({ ok: true, message: texte });
  } catch (err) {
    res.status(409).json({ erreur: err.message });
  }
}

const actions = {
  synchro: [config.commandes.synchro, 'Synchronisation NTP demandée'],
  start: [config.commandes.start, 'Démarrage des mesures'],
  stop: [config.commandes.stop, 'Arrêt des mesures'],
  slowBlink: [config.commandes.slowBlink, 'Clignotement lent'],
  fastBlink: [config.commandes.fastBlink, 'Clignotement rapide'],
};

app.post('/api/command/:action', (req, res) => {
  const action = actions[req.params.action];
  if (!action) return res.status(404).json({ erreur: 'Commande inconnue' });
  publier(res, 'commande', action[0], action[1]);
});

app.post('/api/blink', (req, res) => {
  const periode = parseInt(req.body.periode, 10);
  if (!(periode >= 100 && periode <= 10000)) {
    return res.status(400).json({ erreur: 'Période entre 100 et 10000 ms' });
  }
  try {
    mqtt.publier('blink', periode);
    mqtt.publier('commande', config.commandes.customBlink);
    res.json({ ok: true, message: `Clignotement personnalisé : ${periode} ms` });
  } catch (err) {
    res.status(409).json({ erreur: err.message });
  }
});

app.post('/api/bargraph', (req, res) => {
  const valeur = parseInt(req.body.valeur, 10);
  if (!(valeur >= 0 && valeur <= 1023)) {
    return res.status(400).json({ erreur: 'Valeur entre 0 et 1023' });
  }
  publier(res, 'bargraphe', valeur, `Bargraphe : ${valeur}`);
});

// ---------------- Base de données ----------------
app.get('/api/capteurs', (req, res) => res.json(base.capteurs()));

app.get('/api/plage', (req, res) => {
  res.json(base.plage(req.query.capteur ? Number(req.query.capteur) : null));
});

app.get('/api/mesures', (req, res) => {
  const { debut, fin, capteur } = req.query;
  if (!debut || !fin) return res.status(400).json({ erreur: 'Paramètres debut et fin requis' });
  res.json(base.mesures(debut, fin, capteur ? Number(capteur) : null));
});

// ---------------- Démarrage ----------------
const serveur = app.listen(config.httpPort, () => {
  console.log(`Interface web : http://localhost:${config.httpPort}`);
});

process.on('SIGINT', () => {
  mqtt.deconnecter();
  base.fermer();
  serveur.close(() => process.exit(0));
});
