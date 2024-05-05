import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the router you created
from app.routers.routes import router 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your router
app.include_router(router,prefix="/MOMBOT",tags=["chats,chatbot"])

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
