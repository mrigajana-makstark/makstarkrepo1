from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
# from auth import router as auth_router
# from offer_letter import router as offer_router
# from pdf_generator import router as pdf_router
# ---- JWT Setup ----
# ---- Supabase & JWT Setup ----

SECRET_KEY = "19441678e34d5ff1feef4cd612f5a90858e69e24f1853a5d3cb467d4e422b6a9"                     # <-- Put your JWT secret key here
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

# Dependency to verify JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class OfferRequest(BaseModel):
    name: str
    position: str
    salary: float

class OfferResponse(BaseModel):
    name: str
    position: str
    salary: float
    message: str

@router.post("/generate-offer", response_model=OfferResponse)
def generate_offer(data: OfferRequest, user=Depends(get_current_user)):
    # Example: Calculate salary (could add logic here)
    calculated_salary = data.salary * 1.1  # e.g., add 10% bonus
    return {
        "name": data.name,
        "position": data.position,
        "salary": calculated_salary,
        "message": f"Offer letter generated for {data.name} as {data.position}."
    }