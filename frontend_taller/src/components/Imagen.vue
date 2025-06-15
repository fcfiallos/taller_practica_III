<template>
  <div class="view-container">
    <h2 class="view-title">Sube tu Foto</h2>

    <div v-if="photoSuccess && predictionResult" class="success-message">
      ¡Foto procesada exitosamente! 📸
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div
      class="upload-area"
      :class="{ 'drag-over': isDragOver }"
      @click="triggerFileInput"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      @drop.prevent="handleFileDrop"
    >
      <div class="upload-icon">📁</div>
      <div class="upload-text">
        <strong>Haz clic para seleccionar</strong> o arrastra tu foto aquí
      </div>
      <small style="color: #999">JPG, PNG, GIF hasta 5MB</small>
    </div>

    <input
      type="file"
      class="file-input"
      ref="fileInput"
      @change="handleFileSelect"
      accept="image/*"
    />

    <div v-if="selectedImage" class="preview-container">
      <img :src="selectedImage" alt="Preview" class="preview-image" />
      <br />
      <button @click="removeImage" class="remove-btn">Remover imagen ❌</button>
      <br /><br />
      <button @click="uploadImage" class="submit-btn" :disabled="isLoading">
        <span v-if="!isLoading">Confirmar Subida 📤</span>
        <span v-else>Procesando...</span>
      </button>

      <div v-if="predictionResult" class="results-container">
    <h3>Resultado del análisis:</h3>
    <div class="emotion-results">
      <div class="emotion-row">
        <span class="emotion-label">Emoción detectada:</span>
        <span class="emotion-value">{{ predictionResult}}</span>
      </div>
    </div>
  </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import apiClient from "@/clients/apiClient"; // Asegúrate de que la ruta sea correcta

const imageFile = ref(null);
const selectedImage = ref(null);
const isDragOver = ref(false);
const isLoading = ref(false);
const photoSuccess = ref(false);
const errorMessage = ref("");
const predictionResult = ref(null);

const triggerFileInput = () => {
  errorMessage.value = "";
  photoSuccess.value = false;
  predictionResult.value = null;
  document.querySelector(".file-input").click();
};

const handleFileSelect = (event) => {
  errorMessage.value = "";
  photoSuccess.value = false;
  predictionResult.value = null;
  const file = event.target.files[0];
  processFile(file);
};

const handleFileDrop = (event) => {
  isDragOver.value = false;
  errorMessage.value = "";
  photoSuccess.value = false;
  predictionResult.value = null;
  const file = event.dataTransfer.files[0];
  processFile(file);
};

const processFile = (file) => {
  if (file && file.type.startsWith("image/")) {
    if (file.size > 5 * 1024 * 1024) {
      errorMessage.value = "La imagen no debe superar los 5MB.";
      return;
    }
    imageFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      selectedImage.value = e.target.result;
    };
    reader.readAsDataURL(file);
  } else {
    errorMessage.value = "Por favor selecciona un archivo de imagen válido.";
  }
};

const removeImage = () => {
  imageFile.value = null;
  selectedImage.value = null;
  predictionResult.value = null;
  photoSuccess.value = false;
  errorMessage.value = "";
};

const uploadImage = async () => {
  if (!imageFile.value) {
    errorMessage.value = "No se ha seleccionado ninguna imagen.";
    return;
  }
  isLoading.value = true;
  errorMessage.value = "";
  photoSuccess.value = false;
  predictionResult.value = null;
  try {
    const result = await apiClient.predictEmotion(imageFile.value);
    console.log("Resultado de la API:", result);
        // ...existing code...
    predictionResult.value = result.emoción; // <-- Usa la tilde
    console.log("Resultado de la predicción:", predictionResult.value);
    photoSuccess.value = true;
    // ...existing code...
  } catch (err) {
    errorMessage.value = "Hubo un error al subir la imagen o procesarla.";
  } finally {
    isLoading.value = false;
  }
};

export default {
  setup() {
    return {
      imageFile,
      selectedImage,
      isDragOver,
      isLoading,
      photoSuccess,
      errorMessage,
      predictionResult,
      triggerFileInput,
      handleFileSelect,
      handleFileDrop,
      processFile,
      removeImage,
      uploadImage,
    };
  },
};
</script>

<style scoped>
.view-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.3);
  max-width: 500px;
  width: 100%;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.view-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.upload-area {
  border: 3px dashed #ddd;
  border-radius: 15px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.5);
  margin-bottom: 2rem;
}

.upload-area:hover,
.upload-area.drag-over {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
  transform: scale(1.02);
}

.upload-icon {
  font-size: 3rem;
  color: #ccc;
  margin-bottom: 1rem;
}

.upload-text {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.file-input {
  display: none;
}

.preview-container {
  margin-top: 2rem;
  text-align: center;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: zoomIn 0.3s ease-out;
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.remove-btn {
  background: #ff6b6b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  margin-top: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  background: #ff5252;
  transform: translateY(-1px);
}

.submit-btn {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

.success-message {
  background: linear-gradient(45deg, #4caf50, #8bc34a);
  color: white;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  text-align: center;
  animation: slideInDown 0.5s ease-out;
}
.error-message {
  background: linear-gradient(45deg, #ff6b6b, #ffb199);
  color: white;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  text-align: center;
  animation: slideInDown 0.5s ease-out;
}
@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .view-container {
    padding: 2rem 1.5rem;
    margin: 1rem;
  }
}
</style>