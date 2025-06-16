# /api/app/text_model_handler.py

import tensorflow as tf
import numpy as np
import pickle
import os

# configuracion de carga inicial (se ejecuta una sola vez) 

# Rutas a los artefactos del modelo dentro del contenedor Docker
MODEL_DIR = "/app/models"
VOCAB_PATH = os.path.join(MODEL_DIR, 'vocabulary.pkl')
WEIGHTS_PATH = os.path.join(MODEL_DIR, 'modelo_pesos.weights.h5')

# Parámetros del modelo (deben ser idénticos a los del entrenamiento)
MAX_TOKENS = 15000
OUTPUT_SEQUENCE_LENGTH = 250
embedding_dim = 128

def _load_model_artifacts():
    """Función interna para cargar todo lo necesario para el modelo."""
    print("Cargando artefactos del modelo de texto...")
    
    # Cargar vocabulario
    with open(VOCAB_PATH, 'rb') as f:
        vocabulary = pickle.load(f)

    # Crear la capa de vectorización y cargar el vocabulario
    vectorize_layer = tf.keras.layers.TextVectorization(
        max_tokens=MAX_TOKENS,
        output_sequence_length=OUTPUT_SEQUENCE_LENGTH,
        vocabulary=vocabulary
    )

    # Re-crear la arquitectura del modelo de inferencia
    inference_model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=MAX_TOKENS, output_dim=embedding_dim, mask_zero=True),
        tf.keras.layers.GlobalMaxPooling1D(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Construir el modelo y cargar los pesos
    inference_model.build(input_shape=(None, OUTPUT_SEQUENCE_LENGTH))
    inference_model.load_weights(WEIGHTS_PATH)
    
    print("Modelo de texto cargado y listo.")
    return vectorize_layer, inference_model

# Cargamos el modelo y la capa de vectorización cuando la API se inicia
vectorize_layer, text_model = _load_model_artifacts()


#  FUNCIÓN DE PREDICCIÓN (la que llamará el endpoint) ---

def predict_depression(text: str) -> dict:
    """
    Recibe un texto, lo procesa y devuelve la predicción en un diccionario.
    """
    # Pre-procesar el texto de entrada
    text_vectorized = vectorize_layer([text])
    
    # Realizar la predicción
    prediction = text_model.predict(text_vectorized)
    
    probabilidad_depresion = float(prediction[0][0])
    
    if probabilidad_depresion > 0.5:
        clase = 1
        etiqueta = "Deprimido"
    else:
        clase = 0
        etiqueta = "Normal"
        
    # Formatear la respuesta
    response = {
        'texto_evaluado': text,
        'clasificacion': etiqueta,
        'clase_predicha': clase,
        'confianza': {
            'deprimido': probabilidad_depresion,
            'normal': 1.0 - probabilidad_depresion
        }
    }
    
    return response