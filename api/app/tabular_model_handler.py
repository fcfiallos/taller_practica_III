

import joblib
import pandas as pd
import os



# Rutas a los artefactos dentro del contenedor Docker
MODEL_DIR = "/app/models"
MODEL_PATH = os.path.join(MODEL_DIR, 'mejor_modelo_depresion.joblib')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler_depresion.joblib')
COLUMNS_PATH = os.path.join(MODEL_DIR, 'columnas_modelo_depresion.joblib')

print("Cargando artefactos del modelo tabular de depresión estudiantil...")
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
model_columns = joblib.load(COLUMNS_PATH)
print("✅ Modelo tabular cargado y listo.")

# funcion de prediccion

def predict_student_depression(input_data: dict) -> dict:
    """
    Recibe los datos de un estudiante en un diccionario, los pre-procesa
    y devuelve la predicción del modelo.
    """
    # a. Convertir el diccionario de entrada en un DataFrame de Pandas
    df = pd.DataFrame([input_data])
    
    # b. Reordenar y asegurar que las columnas coincidan con las del entrenamiento
    # Esto es CRUCIAL para evitar errores y garantizar la consistencia.
    df = df.reindex(columns=model_columns, fill_value=0)
    
    # c. Escalar los datos con el scaler que ya fue "entrenado"
    data_scaled = scaler.transform(df)
    
    # d. Realizar la predicción
    prediction = model.predict(data_scaled)
    prediction_proba = model.predict_proba(data_scaled)
    
    # e. Interpretar y formatear el resultado
    clase_predicha = int(prediction[0])
    # La confianza es la probabilidad de la clase predicha
    confianza = prediction_proba[0][clase_predicha]
    etiqueta = "Con Depresión" if clase_predicha == 1 else "Sin Depresión"
    
    response = {
        "clasificacion": etiqueta,
        "clase_predicha": clase_predicha,
        "confianza": float(confianza)
    }
    
    return response