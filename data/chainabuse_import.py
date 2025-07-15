import requests
import json
from pymongo import MongoClient
from datetime import datetime
from app.config import CHAINABUSE_API_KEY, MONGO_URI
from app.utils import guess_chain, get_now_iso

client = MongoClient(MONGO_URI)
col = client["risk_db"]["addresses"]

def fetch_chainabuse_via_api():
    url = "https://api.chainabuse.com/api/reports?limit=20"
    headers = {
        "Authorization": f"Bearer {CHAINABUSE_API_KEY}",
        "Accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    data = res.json()

    for item in data.get("data", []):
        addr = item.get("address")
        if not addr:
            continue
        label = {
            "type": item.get("category", "Reported"),
            "source": "Chainabuse",
            "confidence": "medium",
            "evidence_url": item.get("url", ""),
            "tagged_at": get_now_iso()
        }
        col.update_one(
            {"address": addr},
            {
                "$push": {"labels": label},
                "$set": {
                    "chain": guess_chain(addr),
                    "updated_at": get_now_iso()
                }
            },
            upsert=True
        )

if __name__ == "__main__":
    fetch_chainabuse_via_api()
    print("✅ Chainabuse 数据已同步")
