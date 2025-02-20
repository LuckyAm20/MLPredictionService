import os
from datetime import timedelta

from database.database import get_session
from fastapi import (APIRouter, Depends, File, Form, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from routes.user import UserCreate, deposit_balance, get_token, signin, signup
from services.auth import (create_access_token, get_current_user,
                           get_token_for_user)
from services.crud.prediction import (get_next_prediction_id,
                                      get_predictions_by_user)
from services.crud.transaction import get_transactions_by_user
from services.crud.user import (create_user, get_user_by_username,
                                update_user_balance, update_user_model)
from sqlalchemy.orm import Session
from workers.publisher import publish_prediction_task

web_router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="templates")

@web_router.get("/dashboard")
async def dashboard(request: Request, session: Session = Depends(get_session)):
    user = get_current_user(request, session)

    predictions = get_predictions_by_user(user.id, session)

    transactions = get_transactions_by_user(user.id, session)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "predictions": predictions[::-1],
        "transactions": transactions[::-1],
        "balance": user.balance,
    })


@web_router.post("/balance")
async def deposit_balance_web(amount: int = Form(...), session: Session = Depends(get_session), user=Depends(get_current_user)):
    await deposit_balance(amount, session, user)
    return RedirectResponse(url="/dashboard", status_code=303)


@web_router.post("/select_model")
async def select_model(data: str = Form(...), session: Session = Depends(get_session), user=Depends(get_current_user)):
    update_user_model(user, data, session)
    return RedirectResponse(url="/dashboard", status_code=303)


@web_router.post("/predict")
async def predict_image(file: UploadFile = File(...), session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.selected_model:
        return RedirectResponse(url="/dashboard", status_code=303)

    temp_dir = "/app/temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    image_path = os.path.join(temp_dir, file.filename)
    with open(image_path, "wb") as buffer:
        buffer.write(await file.read())

    prediction_id = get_next_prediction_id(session)
    publish_prediction_task(user, image_path, user.selected_model, 10, prediction_id, session)

    return RedirectResponse(url="/dashboard", status_code=303)


@web_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@web_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@web_router.post("/login")
async def login_user(request: Request, session: Session = Depends(get_session)):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    try:
        auth_response = await signin(UserCreate(username=username, password=password), session)
    except Exception:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверные данные"})

    access_token = create_access_token(data={"sub": str(auth_response['user_id'])}, expires_delta=timedelta(minutes=60))

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    return response


@web_router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@web_router.post("/register")
async def register_user(request: Request, username: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    try:
        user = UserCreate(username=username, password=password)
        await signup(user, session)
        return RedirectResponse(url="/dashboard", status_code=303)
    except HTTPException as e:
        return templates.TemplateResponse("register.html", {"request": request, "error": e.detail})


@web_router.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
