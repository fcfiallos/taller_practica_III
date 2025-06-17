import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // 👈 backend FastAPI corre aquí desde docker-compose
  headers: {
    "Content-Type": "multipart/form-data",
  },
});

export default {
  async predictEmotion(imageFile) {
    const formData = new FormData();
    formData.append("imagen", imageFile);

    try {
      const response = await api.post("/predict/", formData);
      return response.data; // Esperamos algo como { emoción: "Happy" }
    } catch (error) {
      console.error("Error al predecir emoción:", error);
      throw error;
    }
  },
};

// La URL base de tu API. Cambia si es necesario.
const API_URL = 'http://localhost:8000';
// Función para llamar al endpoint de análisis de texto
export const predictText = async (text) => {
  const response= axios.post(`${API_URL}/predict_text/`, {
    texto: text, // El cuerpo de la solicitud en formato JSON
  });
  return response;
};

// Función para llamar al endpoint de análisis de estudiante
export const predictStudent = async (studentData) => {
  // studentData debe ser un objeto JS que coincida con tu modelo Pydantic
  const response= axios.post(`${API_URL}/predict_student/`, studentData);
  return response;
};
