```python
import requests
import csv
from pymongo import MongoClient
from datetime import datetime

OFAC_CSV_URL = "https://www.treasury.gov/ofac/downloads/sdn.csv"
client = MongoClient("mongodb://localhost:27017")
collection = client["risk_db"]["addresses"]

response = requests.get(OFAC_CSV_URL)
with open("sdn.csv", "wb") as f:
    f.write(response.content)

with open("sdn.csv", "r", encoding="latin1") as f:
    reader = csv.reader(f)
    for row in reader:
        for field in row:
            if "0x" in field:
                address = field.strip()
                collection.update_one(
                    {"address": address},
                    {"$push": {"labels": {
                        "type": "OFAC Sanctioned",
                        "source": "OFAC",
                        "confidence": "critical",
                        "evidence_url": None,
                        "tagged_at": datetime.utcnow().isoformat()
                    }}, "$set": {"chain": "ETH", "updated_at": datetime.utcnow().isoformat()}},
                    upsert=True
                )
```
