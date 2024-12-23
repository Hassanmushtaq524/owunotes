from fastapi import APIRouter, HTTPException
from starlette.requests import Request 
from sqlalchemy.orm import Session
from db import db_dependency
import uvicorn 
from google.oauth2 import id_token 
from google.auth.transport import requests 
from models import User
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


router = APIRouter()


class authentication_body(BaseModel):
    token : str

@router.post("/login")
def authentication(request: Request, data: authentication_body, db: Session = db_dependency):
    try:
        # Verify the token with Google's API
        user_data = id_token.verify_oauth2_token(data.token, requests.Request(), GOOGLE_CLIENT_ID)

        # Extract user infoxs
        user_email = user_data["email"]
        user_name = user_data["name"]

        # Check if the user already exists in the database
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            # If user doesn't exist, add them to the database
            new_user = User(
                google_sub=user_data["sub"],  
                name=user_name,
                email=user_email,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user

        # Store user info in session (if needed)
        request.session["user"] = {
            "email": user.email, 
            "name": user.name
        }

        # Return the authenticated user's
        return {
            "status": "success",
            "user": {
                "email": user.email, 
                "name": user.name
            },
            "token": data.token,
        }
    except Exception as e:
        # TODO: remove
        print(e)
        raise HTTPException(status_code=401, detail="Unauthorized")



@router.get("/checksession")
def check_session(request: Request):
    # Check if user session exists
    if request.session.get("user"):
        return {"status": "success", "user": request.session.get("user")}
    else:
        raise HTTPException(status_code=403, detail="Not signed in")