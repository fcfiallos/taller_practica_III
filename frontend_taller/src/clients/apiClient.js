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
