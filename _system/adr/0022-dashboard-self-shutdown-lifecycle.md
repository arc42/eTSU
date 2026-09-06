# 22. Dashboard beendet sich selbst, sobald der Browser-Tab geschlossen wird

Date: 2026-06-22

## Status

Accepted

## Context

Das Requirements-Dashboard (`_system/apps/dashboard/`) ist eine schreibend-lose
Flask-App, die bisher unter gunicorn (2 Worker) in einem Docker-Container im
Hintergrund lief: `dashboard.sh up` → `docker compose up -d`, Restart-Policy
`unless-stopped`, danach öffnet das Skript den Browser.

Daraus folgten zwei Probleme:

- **Kein sauberer Stop aus der Oberfläche.** Beenden ging nur über
  `./dashboard.sh down` bzw. `docker stop` — nichts in der laufenden Web-UI.
- **Browser zu ≠ Server zu.** Schließt man Fenster/Tab, läuft der Container
  unbemerkt weiter (kein WebSocket/SSE/Heartbeat, der das Schließen erkennt),
  belegt Port 8080 und überlebt wegen `unless-stopped` sogar Reboots — eine
  vergessene Waise. Datenverlust droht nicht (read-only), aber der Container
  bleibt als Zombie hängen.

Ein naiver `/stop`-Endpunkt allein löst das nicht: Der gunicorn-Master (PID 1
im Container) startet beendete Worker neu, und `restart: unless-stopped` bringt
den Container nach einem Selbst-Stop sofort wieder hoch — die Restart-Policy
bekämpft aktiv jede Selbstabschaltung von innen.

Außerdem zerfällt In-Memory-Zustand (wer sieht gerade zu?) bei mehreren Workern
in mehrere Prozesse.

Eine **erste Iteration** koppelte Presence an einen dauerhaft offenen
SSE-Stream (`/events`) je Tab — gewählt, weil Hintergrund-Tabs `setInterval`
drosseln/einfrieren und ein naives JS-Heartbeat-Polling deshalb Fehlsignale
liefern kann (Server fährt herunter, obwohl der Tab nur unsichtbar ist). Das
erwies sich als Fehlentscheidung: **jeder offene Stream belegt einen
Worker-Thread für seine gesamte Lebensdauer.** Beim Klicken durch Unterseiten
sammelten sich kurzlebige „Zombie"-Verbindungen (die alte Seite trennt, der
Server merkt es erst beim nächsten Keepalive), bis der Threadpool erschöpft war
— dann ließ sich **nicht einmal mehr `/stop` bedienen** (das Overlay erschien,
der Server starb aber nie). Eine Obergrenze + Thread-Reserve linderte nur das
Symptom. Die eigentliche Frage — *warum überhaupt Verbindungen halten?* —
führte zur Vereinfachung unten.

Auch ein **„Server stoppen"-Knopf** in der UI erwies sich als Sackgasse: Eine
Webseite kann ihren eigenen Tab per Browser-Sicherheitsregel **nicht** schließen
(`window.close()` greift nur bei per Script geöffneten Fenstern). Der Knopf
konnte den Server zwar beenden, ließ aber den toten Tab offen — schlechter, als
einfach den Tab zu schließen. Der Knopf wurde daher wieder entfernt; **das
Schließen des Tabs ist die Beenden-Geste.**

## Decision

Wir behandeln das Dashboard als **kurzlebigen On-Demand-Viewer** (Jupyter-Muster)
und koppeln den Server-Lebenszyklus an „sieht ein Browser zu?".

1. **Presence über leichten Heartbeat — keine gehaltenen Verbindungen.** Jede
   offene Seite schickt alle 20 s ein `POST /ping`; das aktualisiert serverseitig
   nur einen `last seen`-Zeitstempel und kehrt sofort zurück. **Ein /ping hält
   keinen Worker-Thread** — die Threadpool-Erschöpfung der SSE-Variante entfällt
   damit vollständig; wenige Threads genügen. Das Throttling-Problem (der
   ursprüngliche Grund für SSE) wird über eine großzügige Schonfrist gelöst, die
   das Hintergrund-Throttling überdauert (Punkt 2), statt über eine offene
   Verbindung.
2. **Watchdog mit zwei Schonfristen.** Ein Hintergrund-Thread fährt herunter,
   wenn länger als `_HEARTBEAT_GRACE` (90 s) kein `/ping` mehr eintrifft. Die
   Frist ist **bewusst größer als das Browser-Hintergrund-Throttling (~60 s)**:
   ein nur versteckter Tab pingt gedrosselt weiter (~1×/min) und bleibt damit am
   Leben; nur ein wirklich geschlossener Tab pingt gar nicht mehr und löst nach
   der Frist die Abschaltung aus. Sie überbrückt zugleich locker die kurze
   Lücke seiteninterner Navigation. Kommt beim Start nie ein Ping, greift nach
   `_STARTUP_GRACE` (90 s) ebenfalls die Abschaltung, damit ein fehlgeschlagener
   Browser-Start keine Waise hinterlässt. Beide Fristen sind per Env
   (`DASH_HEARTBEAT_GRACE`, `DASH_STARTUP_GRACE`) überschreibbar.
3. **Beenden = Tab schließen, kein Knopf.** Beim Verlassen der Seite feuert ein
   `pagehide`-Beacon `POST /leaving`. Ist es nur **Navigation** zwischen Seiten,
   pingt die Folgeseite sofort wieder und hebt das Signal auf (ein „settle"-Ping
   nach 2,5 s deckt ein spät eintreffendes `/leaving` der Vorseite ab). Ist der
   **Tab/das Fenster wirklich zu**, kommt kein Ping mehr und der Watchdog fährt
   nach `_LEAVE_GRACE` (~5 s) herunter — deutlich schneller als die reine
   Heartbeat-Frist. So genügt die ohnehin gewohnte Geste (Tab schließen) zum
   Beenden; eine Webseite muss ihren eigenen Tab **nicht** schließen (was die
   Browser verbieten). Das Lebenszyklus-Script (Heartbeat + `pagehide`-Beacon)
   liegt in `base.html` und läuft auf jeder Seite. `dashboard.sh` öffnet schlicht
   einen Tab im Standardbrowser (kein App-Modus, kein `--app`).
4. **Sauberes Beenden = SIGTERM an den Master.** `_shutdown()` signalisiert den
   gunicorn-Master (`os.getppid()`); alle Worker steigen aus, PID 1 kehrt
   zurück, der Container endet. Im Dev-Server (`python app.py`) beendet sich der
   Prozess per SIGTERM an sich selbst (NICHT den Parent — das ist die Shell):
   ein aus einem Hintergrund-Thread gesendetes SIGINT verschluckt der
   Werkzeug-Dev-Server (Werkzeug 3.x), SIGTERM greift über die Default-Aktion.
5. **Restart-Policy → `no`.** Nur so bleibt der Container nach Selbst-Stop unten.
   Resilienz über Reboots wird bewusst aufgegeben — ein lokaler Viewer ist kein
   Dienst, der einen Neustart überleben muss.
6. **Ein Worker, kleiner Threadpool** (`gunicorn --worker-class gthread
   --workers 1 --threads 4`). Ein einziger Prozess hält `last seen` und Watchdog
   kohärent. Da **kein Request mehr offen gehalten wird** (der Heartbeat ersetzt
   den SSE-Stream), genügen wenige Threads und der Pool kann nicht mehr erschöpft
   werden — ein paar reichen für einen Seitenaufbau plus den gelegentlichen
   `/ping` nebenher. Das war der Kern des Bugs und ist mit dem Wegfall der
   gehaltenen Verbindung strukturell behoben.

## Consequences

- Tab/Fenster schließen beendet den Server (~5 s über das `pagehide`-Beacon,
  spätestens nach der Heartbeat-Frist): kein verwaister Container, kein dauerhaft
  belegter Port mehr. Das war die Kernsorge.
- Keine UI-Bedienelemente, kein blockierbarer Pool, keine browser-spezifischen
  Fenster-Tricks — die Beenden-Geste ist „Tab zu", die jeder Browser beherrscht.
- **Trade-off:** Navigiert man zwischen Seiten, hängt die Liveness am sofortigen
  Reconnect-Ping; bliebe der aus (z. B. JS deaktiviert), stoppte der Server nach
  `_LEAVE_GRACE`. Für den normalen Betrieb unkritisch.
- **Trade-off:** Schließt man den Tab nur kurz, ist der Server beim Wiederkommen
  evtl. weg und muss per `./dashboard.sh up` neu gestartet werden. Bewusst
  akzeptiert.
- **Trade-off:** Schläft der Rechner länger als die Schonfrist, enden die
  Heartbeats und der Server fährt herunter — derselbe Neustartpfad. Für einen
  lokalen Viewer vertretbar.
- `dashboard.sh down`/`up` bleiben als manueller Fallback gültig; `down` räumt
  einen bereits gestoppten Container ab.
- Reversal hieße: Restart-Policy zurück auf `unless-stopped`, `/ping`+`/leaving`
  +Watchdog entfernt — daher dieser Record.
