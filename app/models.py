```python
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Address Risk Label System")
app.include_router(router)
```
