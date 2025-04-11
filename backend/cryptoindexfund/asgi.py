import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.applications import Starlette

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoindexfund.settings')

fastapi_app = FastAPI()

@fastapi_app.get("/crytpo-index-fund")
async def hello_fastapi():
    return JSONResponse({"message": "Hello from FastAPI"})

django_app = get_asgi_application()

class Application(Starlette):
    def __init__(self):
        super().__init__()
      
        self.mount("/api", fastapi_app)
  
        self.mount("/", django_app)

application = Application()
