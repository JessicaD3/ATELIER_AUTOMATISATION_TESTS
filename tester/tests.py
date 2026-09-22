from .client import ApiClient

API_BASE_URL = "https://api.agify.io"
SLOW_ENDPOINT = "https://httpbin.org/delay/5"


def _resultat(nom, categorie, ok, latence_ms, details):
    return {
        "name": nom,
        "category": categorie,
        "status": "PASS" if ok else "FAIL",
        "latency_ms": round(latence_ms, 2),
        "details": details,
    }


def test_code_http_valide(client):
    resp, lat, err = client.get(params={"name": "michael"})
    ok = resp is not None and resp.status_code == 200
    return _resultat("code_http_valide", "contract", ok, lat, f"HTTP {resp.status_code if resp else err}")


def test_champs_obligatoires(client):
    resp, lat, err = client.get(params={"name": "michael"})
    if resp is None:
        return _resultat("champs_obligatoires", "contract", False, lat, f"Erreur: {err}")
    manquants = {"name", "age", "count"} - resp.json().keys()
    return _resultat("champs_obligatoires", "contract", not manquants, lat, f"Manquants: {sorted(manquants)}")


def test_entree_invalide(client):
    resp, lat, err = client.get(params=None)
    ok = resp is not None and resp.status_code in (400, 422)
    return _resultat("entree_invalide", "contract", ok, lat, f"HTTP {resp.status_code if resp else err}")


def test_config_conforme(client):
    ok = 3.0 <= client.timeout <= 5.0 and client.max_retries == 1
    return _resultat("config_conforme", "robustness", ok, 0.0, f"timeout={client.timeout}s, retries={client.max_retries}")


def test_endpoint_lent_gere(client):
    lent = ApiClient(SLOW_ENDPOINT, timeout=2.0, max_retries=0)
    resp, lat, err = lent.get()
    ok = resp is None and err is not None
    return _resultat("endpoint_lent_gere", "robustness", ok, lat, "Timeout géré sans crash" if ok else "Erreur")


def test_prenom_inconnu(client):
    resp, lat, err = client.get(params={"name": "xyzzyqplonkqwerty"})
    if resp is None:
        return _resultat("prenom_inconnu", "robustness", False, lat, f"Erreur: {err}")
    data = resp.json()
    ok = data.get("age") is None and data.get("count") == 0
    return _resultat("prenom_inconnu", "robustness", ok, lat, f"Réponse: {data}")


TOUS_LES_TESTS = [
    test_code_http_valide,
    test_champs_obligatoires,
    test_entree_invalide,
    test_config_conforme,
    test_endpoint_lent_gere,
    test_prenom_inconnu,
]