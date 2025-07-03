# import uvicorn
# from fastapi import FastAPI
# from app.routes import router
#
# app = FastAPI(title="Basiq API POC")
#
# app.include_router(router)
#
#
# if __name__ == '__main__':
#     uvicorn.run(app, port=8000)

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

from app.routes import router as api_router
from app.services import authenticate, create_user, get_user, get_accounts, generate_consent_url, get_institutions, \
    get_users

app = FastAPI()
app.include_router(api_router, prefix="/api")

templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    token = authenticate()
    users = get_users(token).get("data", [])
    print('users ---> ', users)
    return templates.TemplateResponse("dashboard.html", {"request": request, "users": users})



@app.get("/create-user", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})


@app.post("/create-user", response_class=HTMLResponse)
async def create_user_view(
    request: Request,
    email: str = Form(...),
    mobile: str = Form(...),
    first_name: str = Form(...),
    middle_name: str = Form(""),
    last_name: str = Form(...)
):
    token = authenticate()
    user = create_user(token, email, mobile, first_name, middle_name, last_name)
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})


@app.get("/users")
def list_users():
    token = authenticate()

    return get_users(token)


@app.get("/user/{user_id}", response_class=HTMLResponse)
async def view_user(request: Request, user_id: str):
    token = authenticate()
    user = get_user(token, user_id)
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})


@app.get("/user/{user_id}/consent/{institution_id}", response_class=HTMLResponse)
async def consent(request: Request, user_id: str, institution_id: str):
    token = authenticate()
    url = generate_consent_url(token, user_id, institution_id)
    return templates.TemplateResponse("consent.html", {"request": request, "link": url})


@app.get("/user/{user_id}/accounts", response_class=HTMLResponse)
async def accounts(request: Request, user_id: str):
    token = authenticate()
    return templates.TemplateResponse("accounts.html", {"request": request, "accounts": get_accounts(token, user_id)})


if __name__ == '__main__':
    uvicorn.run(app, port=8000)