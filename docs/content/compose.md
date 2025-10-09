# Docker Compose

Wenn mit mehreren Dockercontainern gleichzeitig in einem Projekt gearbeitet wird,
ist es möglich diese gemeinsam zu bauen, indem man das Tool **Docker Compose** nutzt.

Dazu legen wir (unser letztes Beispiel fortführend) im Hauptverzeichnis die Datei `docker-compose.yml` an:

```title="docker-compose.yml"
services:
  backend:
    image: mysite-backend
    pull_policy: never
    container_name: todo-backend-container
    build:
      context: ./backend
      dockerfile: dockerfile
    ports:
      - 8000:8000

  frontend:
    image: mysite-frontend
    pull_policy: never
    container_name: todo-frontend-container
    build:
      context: ./frontend
      dockerfile: dockerfile
    ports:
      - 80:80
```

Nun können die folgenden Befehle verwendet werden, um alle Container gleichzeitig zu bedienen:

| Befehl | Bedeutung |
|-|-|
| `docker compose build` | Baut alle Images |
| `docker compose up` | Baut alle Container und startet sie. |
| `docker compose down` | Baut fährt alle Container herunter. |
