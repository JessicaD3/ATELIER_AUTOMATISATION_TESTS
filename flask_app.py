from datetime import datetime, timezone

from flask import Flask, render_template, jsonify

import storage
from tester.runner import executer_tous_les_tests

app = Flask(__name__)

DUREE_MIN_ENTRE_RUNS = 5 * 60 


@app.get("/")
def consignes():
    return render_template("consignes.html")


@app.get("/run")
def run():
    dernier = storage.dernier_run()
    if dernier is not None:
        ts = datetime.fromisoformat(dernier["timestamp"])
        ecoule = (datetime.now(ts.tzinfo) - ts).total_seconds()
        if ecoule < DUREE_MIN_ENTRE_RUNS:
            return jsonify({
                "throttled": True,
                "message": f"Dernier run il y a {int(ecoule)}s, réessaie plus tard.",
                "last_run": dernier,
            }), 429

    resultat = executer_tous_les_tests()
    storage.enregistrer_run(resultat)
    return jsonify(resultat)

@app.get("/dashboard")
def dashboard():
    dernier = storage.dernier_run()
    historique = storage.lister_runs(limite=20)
    return render_template(
        "dashboard.html",
        latest=dernier,
        history=historique,
        min_interval_minutes=DUREE_MIN_ENTRE_RUNS // 60,
    )


@app.get("/health")
def health():
    dernier = storage.dernier_run()
    statut = "no_data" if dernier is None else "ok"
    return jsonify({
        "status": statut,
        "last_run_timestamp": dernier["timestamp"] if dernier else None,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)