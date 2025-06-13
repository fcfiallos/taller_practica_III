from pyspark.sql import SparkSession
from pyspark import SparkFiles
import cv2
import numpy as np
import tensorflow as tf
from hdfs import InsecureClient
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

def process_image_and_predict(image_hdfs_path):
    spark = None
    try:
        # Configuración de Spark con más parámetros para estabilidad
        spark = SparkSession.builder \
            .appName("EmotionDetection") \
            .config("spark.submit.deployMode", "client") \
            .config("spark.executor.memory", "1g") \
            .config("spark.driver.memory", "1g") \
            .config("spark.network.timeout", "600s") \
            .getOrCreate()
        
        logger.info("Sesión de Spark iniciada correctamente")
        
        # Configura el modelo
        model_path = "file:///app/models/my_exported_saved_model"
        spark.sparkContext.addFile(model_path)
        
        # Función para procesamiento de imágenes
        def preprocess_image(image_bytes):
            try:
                nparr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                # Convertir a blanco y negro y redimensionar
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                resized_img = cv2.resize(gray_img, (48, 48), interpolation=cv2.INTER_AREA)
                
                # Normalización
                processed_img = resized_img.astype('float32') / 255.0
                processed_img = np.expand_dims(processed_img, axis=-1)
                processed_img = np.expand_dims(processed_img, axis=0)
                
                return processed_img, resized_img
            except Exception as e:
                logger.error(f"Error procesando imagen: {str(e)}")
                raise
        
        # Cliente HDFS con reintentos
        hdfs_client = InsecureClient("http://namenode:9870", user="root", timeout=30)
        
        # Leer imagen de HDFS
        with hdfs_client.read(image_hdfs_path) as reader:
            original_bytes = reader.read()
        
        # Preprocesamiento
        processed_img, resized_img = preprocess_image(original_bytes)
        
        # Guardar versión procesada
        try:
            _, img_bytes = cv2.imencode('.png', resized_img)
            processed_path = image_hdfs_path.replace('/uploads/', '/processed/')
            with tempfile.NamedTemporaryFile() as tmp:
                tmp.write(img_bytes.tobytes())
                hdfs_client.upload(processed_path, tmp.name, overwrite=True)
        except Exception as e:
            logger.warning(f"No se pudo guardar imagen procesada: {str(e)}")
        
        # Cargar modelo y predecir
        model = tf.keras.models.load_model(SparkFiles.get("my_exported_saved_model"))
        prediction = model.predict(processed_img)
        
        return {
            "status": "success",
            "prediction": prediction.tolist()[0],
            "processed_path": processed_path
        }
        
    except Exception as e:
        logger.error(f"Error en process_image_and_predict: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        if spark:
            spark.stop()
            logger.info("Sesión de Spark detenida")