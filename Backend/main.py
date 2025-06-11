from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from routes.plans import router as plans_router
from routes.users import router as users_router
from routes.chat import router as chat_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(plans_router)
app.include_router(users_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Liftology Backend is running!"}
