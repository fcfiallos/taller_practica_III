from pyspark.sql import SparkSession
from pyspark import SparkFiles
from PIL import Image
import os

def preprocess_image(input_path, output_path):
    spark = SparkSession.builder \
        .appName("ImagePreprocessing") \
        .getOrCreate()

    try:
        # Leer imagen
        img = Image.open(input_path).convert("L")  # Escala de grises
        img = img.resize((48, 48))
        
        # Guardar imagen preprocesada
        img.save(output_path)
        print(f"Imagen preprocesada guardada en: {output_path}")
    except Exception as e:
        print("Error en el preprocesamiento:", e)

    spark.stop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Uso: spark-submit preprocess_image.py <input_path> <output_path>")
        sys.exit(1)
    
    preprocess_image(sys.argv[1], sys.argv[2])
