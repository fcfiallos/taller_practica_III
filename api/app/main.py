from fastapi import FastAPI, File, UploadFile
from app.utils import preprocess_image
from pydantic import BaseModel, Field
from typing import Literal 
from hdfs import InsecureClient
import datetime

from app.model_loader import predict_emotion
from app.text_model_handler import predict_depression
from app.tabular_model_handler import predict_student_depression
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
    
#modelo para la entreda de datos del estudiante ( importante este debe contener todos los datos que se espera)
class StudentData(BaseModel):
    Suicidal_Thoughts: Literal[0, 1]
    Academic_Pressure: float
    Financial_Stress: float
    Age: float
    Dietary_Habits: Literal[0, 1, 2]
    Study_Satisfaction: float
    Work_Study_Hours: float
    Family_History_of_Mental_Illness: Literal[0, 1]
    CGPA: float
    Sleep_Duration: Literal[0, 1, 2, 3]

@app.post("/predict/")
async def predict(imagen: UploadFile = File(...)):
    image_bytes = await imagen.read()
    image_array = preprocess_image(image_bytes)
    emotion = predict_emotion(image_array)

    # Guardar imagen cruda en HDFS
    hdfs_url = "http://namenode:9870"  # URL del namenode expuesto en docker-compose
    client = InsecureClient(hdfs_url, user='root')
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    hdfs_path = f"/nuevo/{emotion}/{now}_{imagen.filename}"
    # Crea la carpeta si no existe y sube la imagen
    with client.write(hdfs_path, overwrite=True) as writer:
        writer.write(image_bytes)

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


@app.post("/predict_student/")
async def predict_student(data: StudentData):
    """
    Recibe un JSON con los datos de un estudiante, lo clasifica
    y devuelve la predicción de depresión.
    """
    input_dict = data.dict()
    resultado = predict_student_depression(input_dict)
    return resultado


