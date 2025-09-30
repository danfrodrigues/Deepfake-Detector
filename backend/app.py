from fastapi import FastAPI, File, UploadFile
from model import load_model, predict
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fake Image Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()

@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result, explanation = predict(model, image_bytes)
    return {"prediction": result, "explanation": explanation}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
