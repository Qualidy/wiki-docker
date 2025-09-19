# Image zu Docker Hub pushen & bei Render hosten (mit Beispiel-Dateien)

Im Folgenden bekommst du eine **komplette Schritt-für-Schritt-Anleitung** inkl. **Beispiel-`Dockerfile`** und **`index.html`** für eine kleine statische Website über **Nginx**. Du kannst die Snippets 1:1 übernehmen.

---

## 0) Projektstruktur

Lege einen neuen Ordner an, z. B. `meine-website/`, mit folgendem Inhalt:

```
meine-website/
├─ Dockerfile
├─ index.html
```

---

## 1) Dateien: `Dockerfile` & `index.html`

Kopiere den folgenden Inhalt in die Dateien:

### `Dockerfile`
```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

RUN chown nginx:nginx /usr/share/nginx/html/index.html
```

### `index.html`
```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Willkommen auf meiner ersten Webseite!</h1>

Ich bin ja so froh, endlich Docker zu lernen.

</body>
</html>
```

---

## 2) Anmeldung bei Docker Hub

1. Öffne [:fontawesome-solid-external-link: hub.docker.com](https://www.hub.docker.com/){ target=_blank rel="noopener noreferrer" }und erstelle ein Konto (oder einloggen).
2. Lege ein Repository an: **Hub → Repositories → Create Repository**  
   - Name: `meine-website`  
   - Visibility: Public (oder Private, dann später Token bei Render hinterlegen)

---

## 3) Image lokal bauen & zu Docker Hub pushen

Öffne eine Kommandozeile in deinem Ordner `meine-website` und führe die folgenden Befehle aus.

Baue zunächst das Image:

```bash
docker build -t meine-website:1.0 .
```

Baue lokal den Container uns starte ihn, um ihn zu testen:

```bash
docker run --rm -p 8080:80 meine-website:1.0
```

Um zu prüfen, ob deine Container einwandfrei läuft, kannst du http://localhost:8080 im Browser öffnen.

Melde dich nun bei Docker Hub an, indem du in die Kommandozeile eingibst:

```bash
docker login
```

Damit das hochladen des Images auf Docker Hub korrekt funktioniert, muss du dem Image ein spezielles Tag geben.
Dies kannst du wie folgt tun. 

⚠ Ersetze `DEINUSER` unten durch **deinen** Docker-Hub-Benutzernamen (z. B. `viktorreichert`)

```bash
docker tag meine-website:1.0 DEINUSER/meine-website:1.0
```

Du kannst nun dein Image auf Docker Hub uploaden mit dem folgenden Befehl:

```bash
docker push DEINUSER/meine-website:1.0
```

⚠ Wenn der Upload nicht erlaubt wird, melde dich von Docker Hub ab

```bash
docker logout
```

und danach wieder an.

```bash
docker login
```

Dann sollte der Upload funktionieren.

Gehe auf dein Repository im Docker Hub (drücke ggf. `F5`) und du solltest das hochgeladene Image sehen.

---

## 4) Anmeldung bei Render

1. Öffne [:fontawesome-solid-external-link: https://render.com](https://render.com){ target=_blank rel="noopener noreferrer" } und registriere dich (GitHub/GitLab/E-Mail).
2. Free-Plan reicht für Tests.

---

## 5) Docker-Image bei Render hosten (Web Service)

1. **Dashboard → New + → Web Service**
2. **Deploy an existing image from a registry** wählen.
3. **Registry:** *Docker Hub*  
   - Falls privat: Docker-Hub-Login/Access-Token hinterlegen.
4. **Image URL:**  
   ```
   DEINUSER/meine-website:1.0
   ```
   (optional vollqualifiziert: `docker.io/DEINUSER/meine-website:1.0`)
5. **Region:** EU-Region (z. B. Frankfurt),  
   **Service Type:** Web Service,  
   **Instance Type/Plan:** nach Bedarf (Free für Tests).
6. **Port:** `80` (Nginx bedient Port 80 im Container).
7. **Create Web Service** → Render zieht das Image und startet den Container.
8. Nach dem Deploy bekommst du eine öffentliche URL, z. B.  
   `https://meine-website.onrender.com`

---

**Fertig!**  
Damit hast du eine statische Seite via Nginx als Docker-Image **auf Docker Hub** und hostest dieses Image als **Web Service bei Render**.
