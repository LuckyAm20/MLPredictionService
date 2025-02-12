import uvicorn
from database.database import init_db
from fastapi import FastAPI
from routes.prediction import prediction_router
from routes.transaction import transaction_router
from routes.user import user_router

app = FastAPI(title="ML Service API")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(user_router, prefix="/user")
app.include_router(prediction_router, prefix="/prediction")
app.include_router(transaction_router, prefix="/transaction")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
