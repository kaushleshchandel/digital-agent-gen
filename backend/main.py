from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
# SQLAlchemy 2.0 moves ``declarative_base`` to ``sqlalchemy.orm``.
# Importing from ``sqlalchemy.ext.declarative`` raises a deprecation warning.
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import secrets
import hashlib

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokens = {}

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user_obj = User(username=user.username, password_hash=hash_password(user.password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"id": user_obj.id, "username": user_obj.username}

@app.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_obj = db.query(User).filter(User.username == user.username).first()
    if not user_obj or user_obj.password_hash != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = secrets.token_hex(16)
    tokens[token] = user_obj.id
    return {"token": token}


def get_current_user(token: str):
    user_id = tokens.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

@app.get('/users')
def list_users(token: str, db: Session = Depends(get_db)):
    get_current_user(token)
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username} for u in users]

@app.delete('/users/{user_id}')
def delete_user(user_id: int, token: str, db: Session = Depends(get_db)):
    get_current_user(token)
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
