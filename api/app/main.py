from fastapi import FastAPI, File, UploadFile
from app.utils import preprocess_image
from pydantic import BaseModel
from app.model_loader import predict_emotion
from app.text_model_handler import predict_depression

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

# --- Modelo para validar la entrada de texto ---
class TextItem(BaseModel):
    texto: str

@app.post("/predict/")
async def predict(imagen: UploadFile = File(...)):
    image_bytes = await imagen.read()
    image_array = preprocess_image(image_bytes)
    emotion = predict_emotion(image_array)
    return {"emoción": emotion}

# endopoitn para el modelo de texto
@app.post("/predict_text/")
async def predict_text(item: TextItem):
    """
    Recibe un JSON con un campo "texto", lo clasifica y devuelve los resultados.
    """
    # Llama a tu función de predicción
    resultado = predict_depression(item.texto)
    return resultado
