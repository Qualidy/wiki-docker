# Container live bearbeiten

In diesem Beispiel lernst du Schritt für Schritt, wie man einen Nginx-Webserver als Container im Hintergrund startet, sich mit der Shell in diesen Container verbindet und anschließend die Standard-Webseite bearbeitet.  


## Ablauf

1. **Container starten:**  
   Mit  
   ```bash
   docker run -d --name web-server -p 8080:80 nginx:1.27.0
   ```  
   wird ein Container mit dem Namen `web-server` im Hintergrund gestartet. Das Image basiert auf der Nginx-Version 1.27.0. Durch `-p 8080:80` wird der Port 80 des Containers auf Port 8080 des Hostsystems weitergeleitet, sodass der Webserver von außen erreichbar ist.  

2. **Im Browser öffnen:**  
   Wenn du im Browser `http://localhost:8080` eingibst, sollte die Nginx-Startseite erscheinen. Damit überprüfst du, ob der Container läuft und erreichbar ist.  

3. **In den Container einloggen:**  
   Mit  
   ```bash
   docker exec -it web-server sh
   ```  
   öffnest du eine interaktive Shell innerhalb des Containers. So kannst du direkt mit dem Linux-Dateisystem und den installierten Programmen im Container arbeiten.  

4. **Inhalt auflisten:**  
   Mit  
   ```bash
   ls
   ```  
   siehst du die Dateien und Verzeichnisse im aktuellen Arbeitsverzeichnis des Containers. Das ist nützlich, um dich im Container zu orientieren.  

5. **Vim testen:**  
   Wenn du  
   ```bash
   vim
   ```  
   eingibst, überprüfst du, ob der Texteditor Vim im Container installiert ist. Standardmäßig ist er bei Nginx-Images meist nicht vorhanden.  

6. **Vim installieren:**  
   Falls Vim fehlt, installierst du ihn mit:  
   ```bash
   apt-get update
   apt-get install -y vim
   ```  
   Der erste Befehl aktualisiert die Paketquellen, der zweite installiert den Editor.  

7. **Vim starten und wieder schließen:**  
   Mit  
   ```bash
   vim
   ```  
   öffnest du den Editor. Mit den folgenden Befehlen kannst du Text einfügen, speichern oder abbrechen.  

    !!! tip "Vim-Grundlagen"
        - `i` → **Einfügen starten** (Textbearbeitung möglich)  
        - `Esc` → **zurück in den Normalmodus**  
        - `:wq` → **speichern und beenden**  
        - `:q` → **beenden ohne Speichern (falls keine Änderungen)**  
        - `:q!` → **erzwingen: beenden ohne Speichern**  

8. **Standard-Webseite ansehen:**  
   Mit  
   ```bash
   cat /usr/share/nginx/html/index.html
   ```  
   kannst du dir den Inhalt der Standard-Webseite von Nginx anzeigen lassen.  

9. **Standard-Webseite bearbeiten:**  
   Mit  
   ```bash
   vim /usr/share/nginx/html/index.html
   ```  
   öffnest du die HTML-Datei im Editor. Hier kannst du eigene Änderungen vornehmen, z. B. den Text austauschen.  

10. **Änderungen im Browser prüfen:**  
    Lade nun im Browser die Seite unter `http://localhost:8080` neu. Du solltest sofort deine Änderungen an der Webseite sehen.  

11. **Container-Shell verlassen:**  
    Mit  
    ```bash
    exit
    ```  
    verlässt du die Shell im Container und bist wieder zurück auf deinem Hostsystem.  

---

## Hinweis zu Persistenz

Alle Änderungen, die du direkt im Container machst, sind **nicht dauerhaft**, sobald du den Container entfernst (`docker rm`).  
Wenn du deine Dateien behalten möchtest, solltest du **Docker Volumes** nutzen, um die Daten außerhalb des Containers zu speichern.  

---

??? Dockerfile
    In einem spären Abschnitt wird erklärt, wie man Dockerfiles erstellt.
    Kehre hierher zurück, wenn du diesen Abschnitt gelesen hast.

    Das folgende Dockerfile wird dazu verwendet `index.html` vom Host OS ins Image zu kopieren:

    ```dockerfile
    FROM nginx
    COPY index.html /usr/share/nginx/html/index.html
    RUN chown nginx:nginx /usr/share/nginx/html/index.html
    ```
    