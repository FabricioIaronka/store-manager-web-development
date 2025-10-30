from fastapi import FastAPI
import logging

from src.api.routes import user_routes

app = FastAPI()

app.include_router(user_routes.router)

@app.get("/", tags=["Root"])
def welcome_api():
    return {"msg": "Bem vindo à API do Store Manager. Acesse /docs para ver a documentação"}