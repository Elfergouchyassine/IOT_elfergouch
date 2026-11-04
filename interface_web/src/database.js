const fs = require('fs');
const path = require('path');
const Database = require('better-sqlite3');

// Même schéma que la base de l'IHM Python (IHM/ihm_mqtt_simple/IOT.db)
class BaseIoT {
  constructor(fichier, table) {
    fs.mkdirSync(path.dirname(fichier), { recursive: true });
    this.db = new Database(fichier);
    this.table = table;
    this.db.exec(`CREATE TABLE IF NOT EXISTS ${table} (
      Id_capteur integer, Date text, Version text, Temperature real, Humidite real)`);

    this.stmtInsert = this.db.prepare(`INSERT INTO ${table} VALUES (?, ?, ?, ?, ?)`);
  }

  // "02/11/2026 15:59:57" -> "2026-11-02 15:59:57" (format triable pour BETWEEN)
  static versIso(dateCapteur) {
    const m = /^(\d{2})\/(\d{2})\/(\d{4}) (\d{2}:\d{2}:\d{2})$/.exec(dateCapteur || '');
    return m ? `${m[3]}-${m[2]}-${m[1]} ${m[4]}` : null;
  }

  enregistrer({ idCapteur, date, version, temperature, humidite }) {
    const dateIso = BaseIoT.versIso(date);
    const t = parseFloat(temperature);
    const h = parseFloat(humidite);
    // une valeur pas encore reçue ou mal formée : on n'archive pas
    if (!dateIso || Number.isNaN(t) || Number.isNaN(h)) return false;
    this.stmtInsert.run(idCapteur, dateIso, version, t, h);
    return true;
  }

  // Mesures entre deux dates "AAAA-MM-JJ hh:mm:ss"
  mesures(debut, fin, idCapteur) {
    let sql = `SELECT Id_capteur, Date, Version, Temperature, Humidite FROM ${this.table}
               WHERE Date BETWEEN ? AND ?`;
    const params = [debut, fin];
    if (idCapteur) {
      sql += ' AND Id_capteur = ?';
      params.push(idCapteur);
    }
    return this.db.prepare(sql + ' ORDER BY Date ASC').all(...params);
  }

  // Première et dernière date en base (les dates viennent de l'horloge du capteur, pas du PC)
  plage(idCapteur) {
    const filtre = idCapteur ? ' WHERE Id_capteur = ?' : '';
    const params = idCapteur ? [idCapteur] : [];
    return this.db.prepare(`SELECT MIN(Date) AS debut, MAX(Date) AS fin, COUNT(*) AS total
                            FROM ${this.table}${filtre}`).get(...params);
  }

  capteurs() {
    return this.db.prepare(`SELECT DISTINCT Id_capteur FROM ${this.table} ORDER BY Id_capteur`)
      .all().map((r) => r.Id_capteur);
  }

  fermer() {
    this.db.close();
  }
}

module.exports = BaseIoT;
