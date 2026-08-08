from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models, schemas, auth
from database import engine, get_db

app = FastAPI(
    title="UmbrAI Backend API",
    description="API for UmbrAI Platform",
    version="1.0.0"
)

# إنشاء جداول قاعدة البيانات عند إقلاع السيرفر فقط
@app.on_event("startup")
def startup_db_client():
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("Database startup issue:", e)

# السماح للفرونت إند بالاتصال بالسيرفر (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Online", "message": "Welcome to UmbrAI Backend Services"}

# --- 1. مسار إرسال الرسائل (Contact Form) ---
@app.post("/api/contact", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
def send_message(data: schemas.ContactCreate, db: Session = Depends(get_db)):
    new_message = models.ContactMessage(
        name=data.name,
        email=data.email,
        message=data.message
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

# --- 2. مسار تسجيل حساب جديد (Register) ---
@app.post("/api/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = auth.hash_password(user_data.password)
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- 3. مسار تسجيل الدخول (Login) ---
@app.post("/api/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 4. مسار محمي (لا يفتح إلا برقم الـ Token) ---
@app.get("/api/me")
def get_user_profile(current_user: str = Depends(auth.get_current_user)):
    return {"message": f"Welcome back, {current_user}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
