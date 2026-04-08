from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from ml_models import AgePredictor
import uvicorn

app = FastAPI(title="Age Prediction API", description="A lightweight API for predicting age from face images.")

# Initialize the predictor globally so models are loaded only once on startup
predictor = None

@app.on_event("startup")
def load_models():
    global predictor
    # Will automatically download models if not present
    predictor = AgePredictor()

@app.get("/")
def root():
    return {"message": "Welcome to the Age Prediction API. Use /docs to test endpoints."}

@app.post("/predict")
async def predict_age_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await file.read()
    try:
        predicted_age = predictor.predict_age(content)
        if predicted_age is None:
            return JSONResponse(status_code=400, content={"error": "No face detected in the image."})
        return {"age_bracket": predicted_age}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred processing the image.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
