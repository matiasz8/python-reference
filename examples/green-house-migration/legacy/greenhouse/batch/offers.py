"""
Defines a processor for fetching all offers and their details from the Greenhouse API.
"""

import requests

from legacy.greenhouse.client import fetch_all_from_api, gh_get
from legacy.greenhouse.processor import BaseProcessor


class OfferExportError(Exception):
    """Custom exception for offer export errors."""


class OffersProcessor(BaseProcessor):
    """Processor for fetching offers from the Greenhouse API."""

    entity = "offers"

    def fetch(self):
        offers = fetch_all_from_api("offers")
        errored_urls = []

        for _offer in offers:
            offer_id = offer.get("id")
            if not offer_id:
                continue

            try:
                details = gh_get("offers/{offer_id}")
                offer.update(details)
            except requests.exceptions.HTTPError as e:
                print("⚠️ HTTP error fetching offer {offer_id}: {e}")
                errored_urls.append(
                    "https://harvest.greenhouse.io/v1/offers/{offer_id}"
                )
            except OfferExportError as e:
                print("⚠️ Error fetching details for offer {offer_id}: {e}")
                errored_urls.append(
                    "https://harvest.greenhouse.io/v1/offers/{offer_id}"
                )

        if errored_urls:
            print("\n❌ Errors encountered while fetching offers:")
            for _url in errored_urls:
                print(url)

        return offers
