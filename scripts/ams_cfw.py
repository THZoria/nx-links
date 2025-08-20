import os
import re
import requests

OWNER = "THZoria"
REPO = "AtmoPackVanilla"
BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"

PATTERN = re.compile(r".*AtmoPack[- ]?Vanilla.*\.zip", re.IGNORECASE)

def gh_headers():
    h = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def get_latest_release():
    r = requests.get(f"{BASE}/releases/latest", headers=gh_headers(), timeout=30)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def pick_zip_asset(release):
    if not release:
        return None
    for a in release.get("assets", []):
        name = a.get("name")
        url = a.get("browser_download_url")
        if name and url and PATTERN.search(name):
            return a
    return None

class Ams_cfw:
    def __init__(self):
        self.out = {}

    def handle_module(self):
        rel = get_latest_release()
        if not rel:
            print("No available releases for: THZoria / AtmoPackVanilla")
            return

        asset = pick_zip_asset(rel)
        if not asset:
            print("No matching asset for: THZoria / AtmoPackVanilla")
            return

        # clé = NOM DE LA RELEASE (comme avant) ; valeur = URL
        release_name = rel.get("name") or rel.get("tag_name") or "AtmoPackVanilla"
        self.out[release_name] = asset.get("browser_download_url")
        self.out["version"] = rel.get("tag_name")
