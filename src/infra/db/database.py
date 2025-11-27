import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

var = [DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME]

if not all(var):
    raise ValueError(f"Uma ou mais variáveis de ambiente do banco de dados não foram definidas. Verifique seu arquivo .env")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db_session():
    db = SessionLocal()
    try:
        db.execute(text("RESET app.current_user_id"))
        yield db
    finally:
        db.close()

def get_tenant_session(user_id: int):
    db = SessionLocal()
    try:
        db.execute(text(f"SET app.current_user_id = '{user_id}'"))
        yield db
    finally:
        db.execute(text("RESET app.current_user_id"))
        db.close()
