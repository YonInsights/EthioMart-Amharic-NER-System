from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.responses import JSONResponse
from src.db_operations import get_db 

# Initialize FastAPI app
app = FastAPI()

# Fetch Telegram messages
@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    query = text("SELECT * FROM warehouse.telegram_messages_dw LIMIT 10")
    result = db.execute(query).fetchall()
    
    messages = [
        {
            "id": row[0],
            "message": row[1],
            "sentiment": row[2],
            "subjectivity": row[3],
            "hour_of_day": row[4],
            "day_of_week": row[5],
            "is_weekend": row[6],
            "created_at": row[7]
        }
        for row in result
    ]
    
    return JSONResponse(content={"messages": messages})

# Fetch Object Detection results
@app.get("/detections")
def get_detections(db: Session = Depends(get_db)):
    query = text("SELECT * FROM warehouse.object_detection_dw LIMIT 10")
    result = db.execute(query).fetchall()
    
    detections = [
        {
            "id": row[0],
            "image_file": row[1],
            "box_xmin": row[2],
            "box_ymin": row[3],
            "box_xmax": row[4],
            "box_ymax": row[5],
            "confidence": row[6],
            "class": row[7],
            "detection_time": row[8]
        }
        for row in result
    ]
    
    return JSONResponse(content={"detections": detections})
