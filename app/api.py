import uvicorn
from database.database import init_db
from fastapi import FastAPI
from routes.prediction import prediction_router
from routes.transaction import transaction_router
from routes.user import user_router
from routes.web import web_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="ML Service API")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(user_router, prefix="/user")
app.include_router(prediction_router, prefix="/prediction")
app.include_router(transaction_router, prefix="/transaction")
app.include_router(web_router)


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
