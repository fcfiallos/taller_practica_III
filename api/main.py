from flask import Flask, request, jsonify
from flask_cors import CORS
from hdfs import InsecureClient
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

HDFS_URL = os.environ.get("HDFS_URL", "http://namenode:9870")
client = InsecureClient(HDFS_URL, user='root')

# Cargar modelo al iniciar
model = tf.saved_model.load("/models")

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    filename = file.filename
    hdfs_path = f"/images/{filename}"

    # Subir imagen al HDFS
    client.write(hdfs_path, file, overwrite=True)

    # Leer la imagen desde HDFS
    with client.read(hdfs_path) as reader:
        img = Image.open(reader).convert('RGB').resize((128, 128))
        img_array = np.array(img) / 255.0
        img_array = img_array[np.newaxis, ...]

    # Predicción
    prediction = model(img_array)
    predicted_class = np.argmax(prediction.numpy())

    return jsonify({'prediction': int(predicted_class)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
