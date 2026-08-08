import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./umbra_ai.db")

# إعداد خاص بقواعد بيانات SQLite
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# دالة فتح وإغلاق الاتصال بقاعدة البيانات تلقائياً مع كل طلب
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()