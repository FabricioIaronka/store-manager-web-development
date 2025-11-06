from fastapi import FastAPI

from src.api.routes import user_routes, product_routes, client_routes

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(client_routes.router)

@app.get("/", tags=["Root"])
def welcome_api():
    return {"msg": "Bem vindo à API do Store Manager. Acesse /docs para ver a documentação"}