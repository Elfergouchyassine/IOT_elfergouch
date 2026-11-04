const $ = (id) => document.getElementById(id);

// ---------------- Utilitaires ----------------
function toast(message, erreur = false) {
  const t = $('toast');
  t.textContent = message;
  t.className = `toast visible${erreur ? ' erreur' : ''}`;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { t.className = 'toast'; }, 2500);
}

async function api(url, corps) {
  const options = corps === undefined ? {} : {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(corps),
  };
  const res = await fetch(url, options);
  const donnees = await res.json();
  if (!res.ok) throw new Error(donnees.erreur || res.statusText);
  return donnees;
}

// datetime-local "2026-11-03T11:59:40" <-> SQLite "2026-11-03 11:59:40"
const versSql = (v) => v.replace('T', ' ').padEnd(19, ':00').slice(0, 19);
function versInput(date) {
  const p = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${p(date.getMonth() + 1)}-${p(date.getDate())}T${p(date.getHours())}:${p(date.getMinutes())}:${p(date.getSeconds())}`;
}

// ---------------- Onglets ----------------
document.querySelectorAll('.onglet').forEach((bouton) => {
  bouton.addEventListener('click', () => {
    document.querySelectorAll('.onglet, .vue').forEach((el) => el.classList.remove('actif'));
    bouton.classList.add('actif');
    $(bouton.dataset.vue).classList.add('actif');
    if (bouton.dataset.vue !== 'tableau') ouvrirVue(bouton.dataset.vue);
  });
});

// ---------------- Affichage temps réel ----------------
function afficher(etat) {
  $('badge').textContent = etat.connecte ? `Connecté · capteur ${etat.idCapteur}` : 'Déconnecté';
  $('badge').className = `badge ${etat.connecte ? 'on' : 'off'}`;
  $('btnConnect').disabled = etat.connecte;
  $('btnDisconnect').disabled = !etat.connecte;
  $('commandes').disabled = !etat.connecte;

  $('date').textContent = etat.date !== '?' ? etat.date : '--/--/---- --:--:--';
  $('temperature').textContent = etat.temperature !== '?' ? etat.temperature : '--';
  $('humidite').textContent = etat.humidite !== '?' ? etat.humidite : '--';
  $('version').textContent = etat.version !== '?' ? etat.version : '--';
}

const flux = new EventSource('/api/events');
flux.addEventListener('etat', (e) => afficher(JSON.parse(e.data)));

// ---------------- Connexion ----------------
async function initialiser() {
  const conf = await api('/api/config');
  $('ip').value = conf.host;
  $('port').value = conf.port;
  $('user').value = conf.username;
  $('password').value = conf.password;
  $('idCapteur').value = conf.idCapteur;

  const fin = new Date();
  const debut = new Date(fin.getTime() - 3600 * 1000);   // dernière heure par défaut
  ['debut', 'debutBase'].forEach((id) => { $(id).value = versInput(debut); });
  ['fin', 'finBase'].forEach((id) => { $(id).value = versInput(fin); });
}

$('formConnexion').addEventListener('submit', async (e) => {
  e.preventDefault();
  $('btnConnect').disabled = true;
  try {
    afficher(await api('/api/connect', {
      host: $('ip').value,
      port: Number($('port').value),
      username: $('user').value,
      password: $('password').value,
      idCapteur: Number($('idCapteur').value),
    }));
    toast('Connecté au broker MQTT');
  } catch (err) {
    $('btnConnect').disabled = false;
    toast(err.message, true);
  }
});

$('btnDisconnect').addEventListener('click', async () => {
  afficher(await api('/api/disconnect', {}));
  toast('Déconnecté');
});

// ---------------- Commandes ----------------
async function envoyer(url, corps) {
  try {
    toast((await api(url, corps)).message);
  } catch (err) {
    toast(err.message, true);
  }
}

document.querySelectorAll('[data-cmd]').forEach((bouton) => {
  bouton.addEventListener('click', () => envoyer(`/api/command/${bouton.dataset.cmd}`, {}));
});

$('formBlink').addEventListener('submit', (e) => {
  e.preventDefault();
  envoyer('/api/blink', { periode: Number($('blink').value) });
});

$('bargraph').addEventListener('input', () => { $('bargraphVal').textContent = $('bargraph').value; });
$('formBargraph').addEventListener('submit', (e) => {
  e.preventDefault();
  envoyer('/api/bargraph', { valeur: Number($('bargraph').value) });
});

// ---------------- Base de données ----------------
async function chargerCapteurs() {
  const capteurs = await api('/api/capteurs');
  ['capteurCourbe', 'capteurBase'].forEach((id) => {
    const select = $(id);
    const choix = select.value;
    select.innerHTML = '<option value="">Tous</option>'
      + capteurs.map((c) => `<option value="${c}">${c}</option>`).join('');
    select.value = capteurs.map(String).includes(choix) ? choix : (capteurs[0] ?? '');
  });
}

// Cale l'intervalle sur la dernière heure de données présentes en base.
// Les dates sont celles du capteur (RTC + NTP), qui peuvent différer de l'horloge du PC.
async function calerPlage(idDebut, idFin, capteur) {
  const p = new URLSearchParams(capteur ? { capteur } : {});
  const plage = await api(`/api/plage?${p}`);
  if (!plage.total) return 0;

  const fin = new Date(plage.fin.replace(' ', 'T'));
  const debut = new Date(Math.max(new Date(plage.debut.replace(' ', 'T')), fin - 3600 * 1000));
  $(idDebut).value = versInput(debut);
  $(idFin).value = versInput(fin);
  return plage.total;
}

const formulaires = {
  courbes: { form: 'formCourbes', debut: 'debut', fin: 'fin', capteur: 'capteurCourbe', info: 'infoCourbes' },
  base: { form: 'formBase', debut: 'debutBase', fin: 'finBase', capteur: 'capteurBase', info: 'infoBase' },
};

async function ouvrirVue(vue) {
  const f = formulaires[vue];
  try {
    await chargerCapteurs();
    const total = await calerPlage(f.debut, f.fin, $(f.capteur).value);
    if (!total) {
      $(f.info).textContent = 'La base est vide : connectez-vous au capteur pour archiver des mesures.';
      return;
    }
    $(f.form).requestSubmit();   // affiche directement la dernière heure de données
  } catch (err) {
    toast(err.message, true);
  }
}

function requeteMesures(debut, fin, capteur) {
  const p = new URLSearchParams({ debut: versSql(debut), fin: versSql(fin) });
  if (capteur) p.set('capteur', capteur);
  return api(`/api/mesures?${p}`);
}

$('formBase').addEventListener('submit', async (e) => {
  e.preventDefault();
  try {
    const lignes = await requeteMesures($('debutBase').value, $('finBase').value, $('capteurBase').value);
    $('infoBase').textContent = `${lignes.length} mesure(s)`;
    $('lignes').innerHTML = lignes.map((l) => `<tr><td>${l.Id_capteur}</td><td>${l.Date}</td>`
      + `<td>${l.Version ?? ''}</td><td>${l.Temperature.toFixed(1)}</td><td>${l.Humidite.toFixed(1)}</td></tr>`).join('');
  } catch (err) {
    toast(err.message, true);
  }
});

// ---------------- Courbes ----------------
let graphe = null;

function effacerCourbes() {
  if (graphe) graphe.destroy();
  graphe = null;
  $('infoCourbes').textContent = '';
}

$('btnEffacer').addEventListener('click', effacerCourbes);

$('formCourbes').addEventListener('submit', async (e) => {
  e.preventDefault();
  try {
    const capteur = $('capteurCourbe').value;
    const lignes = await requeteMesures($('debut').value, $('fin').value, capteur);
    effacerCourbes();
    $('infoCourbes').textContent = `${lignes.length} mesure(s) du ${versSql($('debut').value)} au ${versSql($('fin').value)}`;

    const css = getComputedStyle(document.documentElement);
    graphe = new Chart($('graphe'), {
      type: 'line',
      data: {
        labels: lignes.map((l) => l.Date),
        datasets: [
          { label: 'Température (°C)', data: lignes.map((l) => l.Temperature), borderColor: css.getPropertyValue('--temp'), pointRadius: 2 },
          { label: 'Humidité (%)', data: lignes.map((l) => l.Humidite), borderColor: css.getPropertyValue('--humi'), pointRadius: 2 },
        ],
      },
      options: {
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: { title: { display: true, text: `Données capteur IdO ${capteur || '(tous)'}` } },
        scales: { x: { ticks: { maxTicksLimit: 8 } } },
      },
    });
  } catch (err) {
    toast(err.message, true);
  }
});

initialiser();
