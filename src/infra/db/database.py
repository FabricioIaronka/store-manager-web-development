import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, declarative_base, Session

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

def set_rls_on_session_begin(session, transaction, connection):
    """
    Event trigger to sustain the session after the commit
    """
    user_id = session.info.get("user_id")
    
    if user_id:
        connection.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))


event.listen(Session, "after_begin", set_rls_on_session_begin)

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
        db.info["user_id"] = user_id
        
        yield db
    finally:
        # Boa prática: limpar ao fechar
        db.close()
