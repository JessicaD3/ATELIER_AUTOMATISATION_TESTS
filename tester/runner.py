import math
from datetime import datetime, timezone, timedelta
from .client import ApiClient, DEFAULT_TIMEOUT, MAX_RETRIES
from .tests import TOUS_LES_TESTS, API_BASE_URL

NOM_API = "Agify"
FUSEAU = timezone(timedelta(hours=2))


def _percentile_95(valeurs):
    if not valeurs:
        return 0.0
    valeurs = sorted(valeurs)
    k = (len(valeurs) - 1) * 0.95
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return valeurs[int(k)]
    return valeurs[f] + (valeurs[c] - valeurs[f]) * (k - f)


def executer_tous_les_tests():
    client = ApiClient(API_BASE_URL, timeout=DEFAULT_TIMEOUT, max_retries=MAX_RETRIES)

    resultats = []
    for test in TOUS_LES_TESTS:
        try:
            resultats.append(test(client))
        except Exception as exc:
            resultats.append({
                "name": test.__name__,
                "category": "robustness",
                "status": "FAIL",
                "latency_ms": 0.0,
                "details": f"Exception: {exc}",
            })

    reussis = sum(1 for r in resultats if r["status"] == "PASS")
    echoues = sum(1 for r in resultats if r["status"] == "FAIL")
    total = len(resultats)

    latences = [r["latency_ms"] for r in resultats if r["latency_ms"] > 0]
    latence_moy = round(sum(latences) / len(latences), 2) if latences else 0.0
    latence_p95 = round(_percentile_95(latences), 2) if latences else 0.0

    return {
        "api": NOM_API,
        "timestamp": datetime.now(FUSEAU).isoformat(),
        "summary": {
            "passed": reussis,
            "failed": echoues,
            "error_rate": round(echoues / total, 4) if total else 0.0,
            "latency_ms_avg": latence_moy,
            "latency_ms_p95": latence_p95,
            "availability": round(reussis / total, 4) if total else 0.0,
        },
        "tests": resultats,
    }