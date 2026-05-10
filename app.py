import io
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO

app = FastAPI(
    title="Malaria YOLO Object Detector",
    description="API for detecting malaria parasites using YOLOv8 with bounding boxes.",
    version="2.0.0"
)

# Load the newly trained YOLO model
MODEL_PATH = "best.pt"

try:
    model = YOLO(MODEL_PATH)
    print("✅ YOLO Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading YOLO model: {e}")
    model = None

# Note: We no longer need the preprocess_image function because YOLO handles 
# all the resizing and normalization mathematically behind the scenes!

@app.post("/api/predict")
async def predict_cell(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
        
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Invalid image file format.")
            
        # Run YOLO inference
        # Since we only trained for 25 epochs, we drop the confidence threshold to 0.1 
        # to ensure it aggressively highlights suspicious cells even if it isn't 100% sure yet.
        results = model.predict(img, conf=0.1) 
        result = results[0]
        
        detections = []
        highest_parasite_conf = 0.0
        parasite_detected = False
        
        # Parse every bounding box found in the image
        for box in result.boxes:
            # Box coordinates
            x1, y1, x2, y2 = box.xyxy[0].tolist() 
            # Confidence score
            conf = float(box.conf[0]) 
            # Class ID (0=parasite, 1=healthy, etc)
            cls_id = int(box.cls[0]) 
            label = result.names[cls_id]
            
            if "parasite" in label.lower():
                parasite_detected = True
                if conf > highest_parasite_conf:
                    highest_parasite_conf = conf

                detections.append({
                    "label": label,
                    "confidence": conf,
                    "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
                })

        return JSONResponse(content={
            "filename": file.filename,
            "parasite_detected": parasite_detected,
            "parasite_probability": f"{highest_parasite_conf * 100:.2f}%" if parasite_detected else "0.00%",
            "prediction_label": "Parasite" if parasite_detected else "Healthy",
            "detections": detections,
            "image_width": img.shape[1],
            "image_height": img.shape[0]
        })
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Mount the web UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# To run locally: uvicorn app:app --reload
