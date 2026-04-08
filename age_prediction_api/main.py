from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from ml_models import AgePredictor
import uvicorn

app = FastAPI(title="Age Prediction API", description="A lightweight API for predicting age from face images.")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the predictor globally so models are loaded only once on startup
predictor = None

@app.on_event("startup")
def load_models():
    global predictor
    # Will automatically download models if not present
    predictor = AgePredictor()

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/predict")
async def predict_age_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await file.read()
    try:
        predictions = predictor.predict_attributes(content)
        if predictions is None:
            return JSONResponse(status_code=400, content={"error": "No face detected in the image."})
        return predictions
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred processing the image.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
