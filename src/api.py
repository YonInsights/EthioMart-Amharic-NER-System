from fastapi import FastAPI

app = FastAPI(title="Telegram Data API", description="API for accessing Telegram data and object detection results.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Telegram Data API!"}