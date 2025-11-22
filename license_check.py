# license_check.py
import os
import json
import requests

LICENSE_FILE = "license.json"

# URL RAW de ton pastebin
LICENSE_URL = "https://pastebin.com/raw/yourLinkHere"

def load_saved_key():
    if not os.path.exists(LICENSE_FILE):
        return None
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("key")
    except:
        return None

def save_key(key: str):
    try:
        with open(LICENSE_FILE, "w", encoding="utf-8") as f:
            json.dump({"key": key}, f, indent=2)
    except:
        pass

def fetch_online_keys():
    try:
        resp = requests.get(LICENSE_URL, timeout=5)
        if resp.status_code != 200:
            return None
        keys = resp.text.splitlines()
        keys = [k.strip() for k in keys if k.strip()]
        return keys
    except:
        return None

def ensure_license(qt_parent=None) -> bool:
    from PyQt5 import QtWidgets

    online_keys = fetch_online_keys()
    if not online_keys:
        QtWidgets.QMessageBox.critical(
            qt_parent,
            "Erreur licence",
            "Impossible de vérifier la licence.\n"
            "Vérifiez votre connexion internet."
        )
        return False

    saved = load_saved_key()
    if saved and saved in online_keys:
        return True

    tries = 0
    while tries < 3:
        key, ok = QtWidgets.QInputDialog.getText(
            qt_parent,
            "Activation requise",
            "Entrez votre clé d’activation :",
        )
        if not ok:
            return False

        key = key.strip()

        if key in online_keys:
            save_key(key)
            QtWidgets.QMessageBox.information(qt_parent, "Activation", "Clé valide !")
            return True
        else:
            QtWidgets.QMessageBox.warning(
                qt_parent,
                "Clé invalide",
                "Cette clé n’est pas dans la base de données."
            )
            tries += 1

    QtWidgets.QMessageBox.critical(
        qt_parent,
        "Échec",
        "Activation impossible.\nL'application va fermer."
    )
    return False
