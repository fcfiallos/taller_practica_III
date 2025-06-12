from flask import Flask, request, jsonify
import os
import numpy as np
from PIL import Image
import io
import tensorflow as tf
import subprocess

app = Flask(__name__)

# Ruta a tu modelo guardado
MODEL_PATH = "/app/models/my_exported_saved_model"
model = tf.keras.models.load_model(MODEL_PATH)

# Función para ejecutar Spark
def run_spark_preprocess(input_path, output_path):
    spark_submit_cmd = [
        "/opt/bitnami/spark/bin/spark-submit",
        "--master", "spark://spark-master:7077",
        "/app/spark-jobs/preprocess_image.py",
        input_path,
        output_path
    ]
    result = subprocess.run(spark_submit_cmd, capture_output=True, text=True)
    print("Spark stdout:", result.stdout)
    print("Spark stderr:", result.stderr)
    if result.returncode != 0:
        raise Exception("Spark preprocessing failed")

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró imagen'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    # Guardar imagen temporalmente
    temp_input_path = '/app/temp/input.jpg'
    temp_output_path = '/app/temp/output.npy'
    image = Image.open(file.stream)
    image.save(temp_input_path)

    # Ejecutar Spark para preprocesamiento
    try:
        run_spark_preprocess(temp_input_path, temp_output_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Cargar imagen procesada
    img_array = np.load(temp_output_path).astype('float32') / 255.0
    img_array = img_array.reshape(1, 48, 48, 1)

    # Predecir
    prediction = model.predict(img_array)
    predicted_class = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return jsonify({
        'emotion': predicted_class,
        'confidence': round(confidence, 4)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
