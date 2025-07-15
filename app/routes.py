```python
from fastapi import APIRouter
from app.services import get_address_labels

router = APIRouter()

@router.get("/api/address/{address}")
def get_risk(address: str):
    return get_address_labels(address)
```
