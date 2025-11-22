import requests

API_URL = "https://api.gametools.network/bf6/stats/"

def fetch_stats(player_name: str, platform: str):
    """Retourne les stats d'un joueur BF6 (dict) ou None en cas d'erreur."""
    params = {"name": player_name, "platform": platform}
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[API] Erreur: {e}")
        return None
