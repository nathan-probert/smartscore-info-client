import requests
import time


def exponential_backoff_request(
    url, method="get", data=None, json_data=None, max_retries=5, base_delay=1
):
    """
    Makes HTTP requests with exponential backoff retry strategy.

    Args:
        url: URL to send the request to
        method: HTTP method ("get" or "post")
        data: Form data for POST requests
        json_data: JSON data for POST requests
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries in seconds

    Returns:
        Parsed JSON response
    """
    method = method.lower()
    for attempt in range(max_retries):
        try:
            if method == "get":
                response = requests.get(url, timeout=10)
            elif method == "post":
                response = requests.post(url, data=data, json=json_data, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            wait_time = base_delay * (2**attempt)
            print(
                f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time} seconds..."
            )
            time.sleep(wait_time)
    raise Exception("Max retries reached. Request failed.")
