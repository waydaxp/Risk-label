```python
from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["risk_db"]
collection = db["addresses"]

def get_address_labels(address: str):
    result = collection.find_one({"address": address})
    if not result:
        return {"address": address, "risk_score": 0, "labels": []}
    return {
        "address": address,
        "risk_score": len(result.get("labels", [])) * 30,  # 简易打分
        "labels": result.get("labels", [])
    }
```
