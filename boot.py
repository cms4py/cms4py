import uvicorn
from cms4py import asgi

uvicorn.run(asgi.application)
