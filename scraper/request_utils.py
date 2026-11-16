import time

import requests


RETRYABLE_STATUS_CODES = {408, 425, 429, 500, 502, 503, 504}


def safe_request(url, headers=None, proxies=None, timeout=30, retries=3, backoff=1.5):
    """Fetch a URL with bounded retries for transient network/server failures."""
    headers = headers or {
        "User-Agent": "WooCommerceProductResearch/1.0 (+respectful crawler)"
    }
    session = requests.Session()

    for attempt in range(max(1, int(retries))):
        try:
            response = session.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
            )
            if response.status_code == 404:
                return None
            if response.status_code in RETRYABLE_STATUS_CODES:
                if attempt + 1 >= retries:
                    response.raise_for_status()
                retry_after = response.headers.get("Retry-After")
                try:
                    delay = min(30, max(0, float(retry_after))) if retry_after else backoff * (2 ** attempt)
                except ValueError:
                    delay = backoff * (2 ** attempt)
                time.sleep(delay)
                continue

            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response

        except requests.exceptions.RequestException:
            if attempt + 1 >= retries:
                return None
            time.sleep(backoff * (2 ** attempt))
        finally:
            # Response bodies are consumed by the caller when successful.
            pass

    return None
