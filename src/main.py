import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import user_routes, product_routes, client_routes, sale_routes, store_routes, auth_routes

load_dotenv()

app = FastAPI()

origins_str = os.getenv("ALLOWED_ORIGINS", "")  
origins = [origin.strip() for origin in origins_str.split(",") if origin.strip()]

if not origins:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(store_routes.router)
app.include_router(product_routes.router)
app.include_router(client_routes.router)
app.include_router(sale_routes.router)
app.include_router(auth_routes.router)

@app.get("/", tags=["Root"])
def welcome_api():
    return {"msg": "Bem vindo à API do Store Manager. Acesse /docs para ver a documentação"}