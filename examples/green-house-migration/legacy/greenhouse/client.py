"""Client for Greenhouse API"""

import time
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

from config import BATCH_SIZE, GREENHOUSE_API_KEY, GREENHOUSE_API_URL

# Configurar sesión con retry y rate limiting
session = requests.Session()
session.auth = (GREENHOUSE_API_KEY, "")

# Configurar retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Rate limiting: Greenhouse permite 50 requests por 10 segundos
RATE_LIMIT_DELAY = 0.2  # 200ms entre requests


def gh_get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetch raw data from the Greenhouse API with rate limiting."""
    url = "{GREENHOUSE_API_URL}/{path.lstrip('/')}"

    # Rate limiting
    time.sleep(RATE_LIMIT_DELAY)

    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            # Rate limit exceeded, wait longer
            time.sleep(2)
            return gh_get(path, params)  # Retry once
        raise


def paginated_get(path: str, pagination: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch paginated data from the Greenhouse API."""
    result = gh_get(path, params=pagination)

    if isinstance(result, list):
        metadata_obj = {"count": len(result), **pagination}
        return {"data": result, "metadata": metadata_obj}
    return {
        "data": [result],
        "metadata": {
            "count": 1,
            "note": "Non-paginated response",
            **pagination,
        },
    }


def fetch_all_from_api(path: str) -> List[Dict[str, Any]]:
    """Fetch all data from a paginated Greenhouse API endpoint."""
    all_data = []
    page = 1
    progress_bar = tqdm(desc="{path}", unit=" page")

    while True:
        result = gh_get(path, params={"per_page": BATCH_SIZE, "page": page})
        items = result.get("data", []) if isinstance(result, dict) else result

        if not items:
            break
        all_data.extend(items)
        progress_bar.update(1)
        page += 1

    progress_bar.close()
    return all_data
