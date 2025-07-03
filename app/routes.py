from fastapi import APIRouter, HTTPException, Body

from app.services import authenticate, get_user, get_accounts, generate_consent_url, create_user, get_institutions

router = APIRouter()


@router.get("/auth")
def auth_token():
    token = authenticate()
    if not token:
        raise HTTPException(status_code=500, detail="Authentication failed")
    return {"access_token": token}


@router.post("/user")
def user(
    email=Body(),
    mobile=Body(),
    firstName=Body(),
    middleName=Body(),
    lastName=Body()
):
    token = authenticate()
    if not token:
        raise HTTPException(status_code=500, detail="Authentication failed")
    return create_user(token, email, mobile, firstName, middleName, lastName)


@router.get("/user/{user_id}")
def user(user_id: str):
    token = authenticate()
    if not token:
        raise HTTPException(status_code=500, detail="Authentication failed")
    return get_user(token, user_id)


@router.get("/user/{user_id}/accounts")
def accounts(user_id: str):
    token = authenticate()
    if not token:
        raise HTTPException(status_code=500, detail="Authentication failed")
    return get_accounts(token, user_id)


@router.get("/user/{user_id}/start-consent/{institution_id}")
def start_consent(user_id: str, institution_id: str):
    token = authenticate()
    consent_url = generate_consent_url(token, user_id, institution_id)
    return {"user_id": user_id, "consent_url": consent_url}


@router.get("/institutions")
def institutions():
    token = authenticate()
    if not token:
        raise HTTPException(status_code=500, detail="Authentication failed")
    return get_institutions(token)
