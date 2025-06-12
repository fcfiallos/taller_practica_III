import axios from 'axios'

const API_URL = "http://localhost:5000";

export async function predictEmotion(file) {
  const formData = new FormData();
  formData.append("image", file);

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Error en la predicción");

    const data = await response.json();
    return data.prediction;
  } catch (error) {
    console.error("Error al predecir:", error);
    throw error;
  }
}
