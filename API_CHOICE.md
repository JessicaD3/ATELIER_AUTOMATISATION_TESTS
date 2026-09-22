# API Choice

- Étudiant : JessicaLP3
- API choisie : Agify (prédiction d'âge à partir d'un prénom)
- URL base : https://api.agify.io
- Documentation officielle / README : https://agify.io/our-apis
- Auth : None
- Endpoints testés :
  - GET /?name=michael
  - GET /?name=xyzzyqplonkqwerty (nom inconnu)
  - GET / (sans paramètre, cas d'erreur)
- Hypothèses de contrat (vérifiées par les tests, run du 22/09/2026) :
  - GET avec name valide → HTTP 200, JSON {name, age, count} tous présents ✅
  - GET avec name inconnu → HTTP 200, age:null, count:0 (pas d'erreur) ✅
  - GET sans name → HTTP 400 ✅
  - Latence observée : moyenne 480.96 ms, p95 1663.67 ms (le p95 est tiré vers
    le haut par le test volontaire d'endpoint lent, qui n'appelle pas Agify)
- Limites / rate limiting connu :
  - Gratuit : 1000 req/jour, 100 req/mois sans compte. Largement suffisant
    (6 requêtes par run, anti-spam 1 run manuel max / 5 min).
- Risques :
  - Service tiers gratuit, pas de SLA → surveillé via le dashboard QoS.
  - Aucune erreur ni timeout rencontré lors du premier run réel.