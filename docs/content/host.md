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
```

### `index.html`
```html
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Meine Website – Hallo Render + Docker Hub</title>
  <style>
    :root { --bg: #0f172a; --fg: #e2e8f0; --accent:#38bdf8; }
    html,body { height:100%; margin:0; font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,"Helvetica Neue",sans-serif; background:var(--bg); color:var(--fg); }
    .wrap { min-height:100%; display:flex; align-items:center; justify-content:center; text-align:center; padding:3rem; }
    h1 { font-size:clamp(2rem, 5vw, 3rem); margin:0 0 1rem; }
    p { opacity:.9; max-width:60ch; margin:0 auto 1.5rem; line-height:1.6; }
    .badge { display:inline-block; padding:.5rem 1rem; border:1px solid var(--accent); color:var(--accent); border-radius:999px; font-weight:600; letter-spacing:.02em; }
    a { color:var(--accent); text-decoration:none; }
    a:hover { text-decoration:underline; }
  </style>
</head>
<body>
  <div class="wrap">
    <main>
      <div class="badge">Docker + Nginx + Render</div>
      <h1>Es läuft! 🚀</h1>
      <p>Diese statische Seite wird aus einem <strong>Docker Image</strong> mit <strong>Nginx</strong> ausgeliefert.
         Das Image liegt auf <strong>Docker Hub</strong> und wird auf <strong>Render</strong> gehostet.</p>
      <p>Viel Erfolg beim Deployment! ✨</p>
    </main>
  </div>
</body>
</html>
```

---

## 2) Anmeldung bei Docker Hub

1. Öffne **https://hub.docker.com** und erstelle ein Konto (oder einloggen).
2. Lege ein Repository an: **Hub → Repositories → Create Repository**  
   - Name: `meine-website`  
   - Visibility: Public (oder Private, dann später Token bei Render hinterlegen)

---

## 3) Image lokal bauen & zu Docker Hub pushen

Öffne eine Kommandozeile in deinem Ordner `meine-website` und führe die folgenden Befehle aus.

Baue zunächst das Image:

```bash
docker build -t meine-website:3.0 .
```

Baue lokal den Container uns starte ihn, um ihn zu testen:

```bash
docker run --rm -p 8080:80 meine-website:3.0
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
docker tag meine-website:3.0 DEINUSER/meine-website:3.0
```

Du kannst nun dein Image auf Docker Hub uploaden mit dem folgenden Befehl:

```bash
docker push DEINUSER/meine-website:3.0
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

1. Öffne **https://render.com** und registriere dich (GitHub/GitLab/E-Mail).
2. Free-Plan reicht für Tests.

---

## 5) Docker-Image bei Render hosten (Web Service)

1. **Dashboard → New + → Web Service**
2. **Deploy an existing image from a registry** wählen.
3. **Registry:** *Docker Hub*  
   - Falls privat: Docker-Hub-Login/Access-Token hinterlegen.
4. **Image URL:**  
   ```
   DEINUSER/meine-website:3.0
   ```
   (optional vollqualifiziert: `docker.io/DEINUSER/meine-website:3.0`)
5. **Region:** EU-Region (z. B. Frankfurt),  
   **Service Type:** Web Service,  
   **Instance Type/Plan:** nach Bedarf (Free für Tests).
6. **Port:** `80` (Nginx bedient Port 80 im Container).
7. **Create Web Service** → Render zieht das Image und startet den Container.
8. Nach dem Deploy bekommst du eine öffentliche URL, z. B.  
   `https://meine-website.onrender.com`

---

## 6) Hinweise & Troubleshooting

- **Port/Health:** Das Nginx-Image lauscht auf `80`. In Render deshalb **Port 80** konfigurieren.  
- **Private Images:** In den Service-Settings bei Render **Docker Hub Credentials** hinterlegen (Username + Access Token mit `read:packages`).  
- **Image nicht gefunden?** Prüfe Tag/Name exakt (alles kleingeschrieben).  
- **Neu deployen:** In Render → Service öffnen → **Manual Deploy → Deploy latest image**.  
- **Logs prüfen:** In Render → Service → **Logs**.

---

## 7) Optional: Automatisch neu bauen (CI)

Wenn deine Seite sich ändert, baue lokal neu und pushe den gleichen Tag oder nutze **versionierte Tags** (z. B. `3.1`, `3.2`) und aktualisiere in Render den Tag. Alternativ kannst du Render „Auto-Deploy latest image“ aktivieren (wenn unterstützt).

---

**Fertig!**  
Damit hast du eine statische Seite via Nginx als Docker-Image **auf Docker Hub** und hostest dieses Image als **Web Service bei Render**.
