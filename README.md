# Equipment Management API

Cloud-native backend for the Department of Environmental Science equipment
loan system. Built with FastAPI, PostgreSQL and SeaweedFS (S3-compatible
object storage), all orchestrated with Docker Compose.

## Running it

1. Copy the environment template:
   ```
   cp .env.example .env
   ```
2. Start everything:
   ```
   docker compose up
   ```
3. Open the interactive API docs at http://localhost:8000/docs

No manual setup beyond `docker compose up` is required — database tables and
the SeaweedFS bucket are created automatically on startup.

## Project layout

```
app/
  main.py          FastAPI app, startup hooks
  database.py       SQLAlchemy engine/session
  models.py         Equipment, Booking, Document ORM models
  schemas.py         Pydantic request/response models
  storage.py         SeaweedFS (S3-compatible) upload/download helpers
  routers/
    equipment.py      Equipment CRUD
    bookings.py       Booking create/list/cancel + overlap prevention
    documents.py       Document upload/list/download
docker-compose.yml   api + db + seaweedfs services
Dockerfile           FastAPI app image
.env.example         required environment variables
```

## What's implemented

- Equipment: create, list, retrieve one, update
- Bookings: create (rejects overlapping active bookings for the same
  equipment), list (filterable by equipment, optionally include cancelled),
  cancel
- Documents: upload (stored in SeaweedFS, metadata in Postgres), list per
  equipment item, download

## Still to do

- Write the screen recording demonstrating `docker compose up` and the
  OpenAPI docs
- Decide whether you want extra validation (e.g. equipment can't be booked
  by its own overlapping booking edge cases), and any deployment polish

## Working as a group of three on GitHub

1. One person creates a new **private** repository on GitHub and pushes this
   folder as the first commit:
   ```
   git init
   git add .
   git commit -m "Initial project scaffold"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
2. The other two clone it:
   ```
   git clone <your-repo-url>
   ```
3. Everyone works on a separate branch per feature/area (matches the split
   suggested earlier — API/DB, storage/Docker, Compose/submission), e.g.:
   ```
   git checkout -b feature/documents-router
   ```
4. Push your branch and open a Pull Request into `main` on GitHub so the
   other two can review before merging — this also gives you a visible
   history of who built what, useful if your group needs to show individual
   contribution.
5. `.env` is already excluded via `.gitignore` — never commit real
   passwords. Everyone creates their own local `.env` from `.env.example`.
6. Before submission, do a **clean clone** on a machine (or fresh folder)
   that's never had this project on it, and confirm `docker compose up`
   works with zero manual steps — this is the same test your marker will
   effectively run.

## Where each piece follows its technology's own documentation

Nothing here is a novel pattern — each file follows the standard approach
recommended by that technology's own docs, which is worth knowing if you
need to extend anything or explain a design choice:

- **FastAPI** — `app/routers/*.py` follow FastAPI's own
  [dependency injection pattern](https://fastapi.tiangolo.com/tutorial/dependencies/)
  (`Depends(get_db)`) and [SQL database tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)
  structure (routers, one dependency yielding a session per request).
- **SQLAlchemy** — `app/models.py` uses the
  [declarative mapping](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
  style (`Base`, `Column`, `relationship`); `app/database.py` uses the
  standard `sessionmaker` + `engine` setup from SQLAlchemy's own quickstart.
- **boto3 / SeaweedFS** — `app/storage.py` uses boto3's
  [S3 client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
  exactly as you would against real AWS S3, just pointed at SeaweedFS's
  `S3_ENDPOINT_URL` — this is what "S3-compatible" means in practice.
- **Docker / Docker Compose** — `Dockerfile` follows Docker's standard
  Python image pattern; `docker-compose.yml` uses the
  [Compose spec](https://docs.docker.com/compose/compose-file/) `depends_on`
  with `condition: service_healthy` so the API waits for Postgres to be
  ready before starting.
