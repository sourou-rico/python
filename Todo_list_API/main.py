from fastapi import FastAPI
from app.routes import todo_routes

app = FastAPI(
    title="Todo List API",
    description="un simple todo list API",
    version="1.0",
    
)

app.include_router(todo_routes.router)
