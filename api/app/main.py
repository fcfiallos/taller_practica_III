from fastapi import FastAPI, File, UploadFile
from app.utils import preprocess_image
from app.model_loader import predict_emotion
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permite solicitudes desde localhost:5173 (puerto de Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict/")
async def predict(imagen: UploadFile = File(...)):
    image_bytes = await imagen.read()
    image_array = preprocess_image(image_bytes)
    emotion = predict_emotion(image_array)
    return {"emoción": emotion}
