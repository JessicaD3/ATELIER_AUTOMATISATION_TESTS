import time
import requests

DEFAULT_TIMEOUT = 4.0
MAX_RETRIES = 1


class ApiClient:
    def __init__(self, base_url, timeout=DEFAULT_TIMEOUT, max_retries=MAX_RETRIES):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def get(self, path="", params=None, timeout=None):
        url = f"{self.base_url}{path}" if path else self.base_url
        effective_timeout = timeout if timeout is not None else self.timeout
        attempt = 0
        last_error = None

        while attempt <= self.max_retries:
            start = time.perf_counter()
            try:
                response = requests.get(url, params=params, timeout=effective_timeout)
                latency_ms = round((time.perf_counter() - start) * 1000, 2)

                if response.status_code in (429, 500, 502, 503) and attempt < self.max_retries:
                    time.sleep(1.0)
                    attempt += 1
                    continue

                return response, latency_ms, None

            except requests.exceptions.RequestException as exc:
                latency_ms = round((time.perf_counter() - start) * 1000, 2)
                last_error = exc
                if attempt < self.max_retries:
                    attempt += 1
                    continue
                return None, latency_ms, exc

        return None, 0.0, last_error