import requests
import time

def safe_request(url, headers, proxies=None):
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"Skipping invalid URL: {url}")
                return None
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
        except requests.exceptions.ReadTimeout as e:
            print(f"Read timeout for {url}, attempt {attempt + 1}: {e}")
            time.sleep(2)
    print(f"Failed to retrieve {url} after multiple attempts.")
    return None
