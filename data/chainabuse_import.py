```python
import requests
import json
from pymongo import MongoClient
from datetime import datetime

API_KEY = "ca_eVFyanZseDI0NmRMeTV6VzlhZlh6MmhqLmpsd1crVUJTV0xtb3BrRG1mMG94Q3c9PQ"
client = MongoClient("mongodb://localhost:27017")
col = client["risk_db"]["addresses"]

def fetch_chainabuse_via_api():
    url = "https://api.chainabuse.com/api/reports?limit=20"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
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
            "tagged_at": datetime.utcnow().isoformat()
        }
        col.update_one(
            {"address": addr},
            {"$push": {"labels": label}, "$set": {"chain": "ETH", "updated_at": datetime.utcnow().isoformat()}},
            upsert=True
        )

if __name__ == "__main__":
    fetch_chainabuse_via_api()
    print("✅ Chainabuse 数据已同步")
```
