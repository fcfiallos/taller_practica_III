import os
import uuid
import tempfile
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from hdfs_utils import HDFSClient
import tensorflow as tf
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

MODEL_PATH = 'models/my_exported_saved_model'
model = tf.keras.layers.TFSMLayer(MODEL_PATH, call_endpoint='serving_default')

HDFS_URL = "http://namenode:9870"
HDFS_UPLOAD_DIR = "/uploads"
hdfs_client = HDFSClient(HDFS_URL)

@app.post("/predict")
async def predict_emotion(file: UploadFile = File(...)):
    try:
        if not (
            file.content_type in ["image/jpeg", "image/png"]
            or file.filename.lower().endswith((".jpg", ".jpeg", ".png"))
        ):
            raise HTTPException(400, "Solo se aceptan imágenes JPG, JPEG o PNG")
        
        # Leer y procesar la imagen directamente
        img = Image.open(file.file).convert("L")
        img = img.resize((48, 48))
        
        # Guardar temporalmente para HDFS
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            img.save(tmp, format="PNG")
            tmp.flush()
            local_path = tmp.name
        
        # Subir a HDFS
        hdfs_filename = f"{uuid.uuid4()}.png"
        hdfs_path = f"{HDFS_UPLOAD_DIR}/{hdfs_filename}"
        hdfs_client.save_file(hdfs_path, local_path)
        
        # Procesar para predicción
        img_array = np.array(img).astype("float32") / 255.0
        img_array = np.expand_dims(img_array, axis=(0, -1)) 
        img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)

        prediction = model(img_tensor).numpy()
        
        os.remove(local_path)
        return {
            "status": "success",
            "prediction": prediction.tolist()[0],
            "hdfs_path": hdfs_path
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}