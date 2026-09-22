import json
import sqlite3
from pathlib import Path

CHEMIN_DB = Path(__file__).parent / "runs.db"


def _connexion():
    conn = sqlite3.connect(CHEMIN_DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connexion()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def enregistrer_run(run: dict):
    conn = _connexion()
    conn.execute(
        "INSERT INTO runs (api, timestamp, payload) VALUES (?, ?, ?)",
        (run["api"], run["timestamp"], json.dumps(run, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()


def lister_runs(limite: int = 20):
    conn = _connexion()
    lignes = conn.execute(
        "SELECT payload FROM runs ORDER BY id DESC LIMIT ?", (limite,)
    ).fetchall()
    conn.close()
    return [json.loads(l["payload"]) for l in lignes]


def dernier_run():
    runs = lister_runs(limite=1)
    return runs[0] if runs else None


init_db()