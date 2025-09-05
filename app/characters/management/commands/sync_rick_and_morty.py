import time
import requests
from datetime import datetime
from urllib.parse import urlencode
from tenacity import retry, wait_exponential, stop_after_delay, retry_if_exception_type
from django.core.management.base import BaseCommand
from characters.models import Character


API_BASE = "https://rickandmortyapi.com/api/character"


class RateLimitError(Exception):
    pass

def _should_keep(result):

    """Apply post-filter to ensure origin variants like 'Earth (C-137)'."""
    origin_name = (result.get("origin") or {}).get("name") or ""
    return (
        result.get("species", "").lower() == "human"
        and result.get("status", "").lower() == "alive"
        and origin_name.startswith("Earth (")
    )

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_delay(120),
    retry=retry_if_exception_type((RateLimitError, requests.RequestException)),
    reraise=True,
)

def _get(url):

    resp = requests.get(url, timeout=20)
    if resp.status_code == 429:

        # Respect Retry-After if present
        retry_after = int(resp.headers.get("Retry-After", "1"))
        time.sleep(retry_after)
        raise RateLimitError("Upstream rate limited")
    resp.raise_for_status()
    return resp.json()

class Command(BaseCommand):

    help = "Sync filtered Rick and Morty characters into local DB"

    def handle(self, *args, **options):

        # Initial query params (server-side filters reduce payload)
        params = {"species": "Human", "status": "Alive"}
        url = f"{API_BASE}?{urlencode(params)}"
        seen = 0
        created = 0
        updated = 0

        while url:
            data = _get(url)
            for item in data.get("results", []):
                if not _should_keep(item):
                    continue
                obj, is_created = Character.objects.update_or_create(
                    id=item["id"],
                    defaults={
                        "name": item.get("name", ""),
                        "status": item.get("status", ""),
                        "species": item.get("species", ""),
                        "type": item.get("type", ""),
                        "gender": item.get("gender", ""),
                        "origin_name": (item.get("origin") or {}).get("name", ""),
                        "origin_url": (item.get("origin") or {}).get("url", ""),
                        "location_name": (item.get("location") or {}).get("name", ""),
                        "location_url": (item.get("location") or {}).get("url", ""),
                        "image": item.get("image", ""),
                        "url": item.get("url", ""),
                        "created": datetime.fromisoformat(item.get("created").replace("Z", "+00:00")),
                    },
                )
                seen += 1
                if is_created:
                    created += 1
                else:
                    updated += 1
            url = (data.get("info") or {}).get("next")
        self.stdout.write(self.style.SUCCESS(
            f"Synced {seen} (created={created}, updated={updated}) Human+Alive with Earth-origin entries"
        ))