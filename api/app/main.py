from fastapi import FastAPI, File, UploadFile
from app.utils import preprocess_image
from app.model_loader import predict_emotion

app = FastAPI()

@app.post("/predict/")
async def predict(imagen: UploadFile = File(...)):
    image_bytes = await imagen.read()
    image_array = preprocess_image(image_bytes)
    emotion = predict_emotion(image_array)
    return {"emoción": emotion}
