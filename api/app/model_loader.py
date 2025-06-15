import json
import numpy as np
from keras.layers import TFSMLayer

# Cargar modelo usando TFSMLayer
model = TFSMLayer("models/my_exported_saved_model", call_endpoint="serving_default")

# Leer las clases
with open("app/emociones_imagenes.json", "r") as f:
    clases = json.load(f)

# Realiza la predicción
def predict_emotion(image_array):
    prediction = model(image_array)  # No necesitas model.predict()
    emotion_index = int(np.argmax(prediction))
    return clases[emotion_index]
