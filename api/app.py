from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from spark_jobs import process_image_and_predict
from hdfs_utils import HDFSClient
import uuid
import os
import tempfile
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuración CORS más permisiva para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Configuración HDFS
HDFS_UPLOAD_DIR = "/uploads"
HDFS_PROCESSED_DIR = "/processed"

@app.post("/predict")
async def predict_emotion(file: UploadFile = File(...)):
    try:
        # 1. Validar tipo de archivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "Solo se aceptan imágenes")
        
        # 2. Leer contenido
        file_bytes = await file.read()
        
        # 3. Guardar original en HDFS
        hdfs_client = HDFSClient("http://namenode:9870")
        file_ext = os.path.splitext(file.filename)[1] or '.jpg'
        hdfs_path = f"{HDFS_UPLOAD_DIR}/{uuid.uuid4()}{file_ext}"
        
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            hdfs_client.save_file(hdfs_path, tmp.name)
        
        # 4. Procesar y predecir
        result = process_image_and_predict(hdfs_path)
        
        if result["status"] != "success":
            raise HTTPException(500, result["message"])
        
        return result
        
    except Exception as e:
        raise HTTPException(500, str(e))
    
# ...existing code...

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
# ...existing code...