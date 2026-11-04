const path = require('path');

// Paramètres par défaut (les mêmes que l'IHM PySide6)
module.exports = {
  httpPort: process.env.PORT || 3000,

  mqtt: {
    host: '192.168.1.1',
    port: 1883,
    username: 'mos_user',
    password: 'mos_user',
  },

  idCapteur: 42920,

  database: path.join(__dirname, '..', 'data', 'IOT.db'),
  table: 'IOT_Data',

  // Codes commande du capteur
  commandes: {
    synchro: 10,
    start: 20,
    stop: 30,
    slowBlink: 40,
    fastBlink: 50,
    customBlink: 60,
  },
};
