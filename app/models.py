```python
from pydantic import BaseModel
from typing import List, Optional

class RiskLabel(BaseModel):
    type: str
    source: str
    evidence_url: Optional[str] = None
    confidence: str
    tagged_at: str

class AddressProfile(BaseModel):
    address: str
    chain: str
    labels: List[RiskLabel]
    updated_at: str
```
