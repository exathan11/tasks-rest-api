from fastapi import FastAPI

from .routers import tasks

app = FastAPI(root_path="/api/v1")

app.include_router(tasks.router)
