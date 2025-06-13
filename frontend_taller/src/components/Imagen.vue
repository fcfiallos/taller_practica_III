<template>
  <div class="view-container">
    <h2 class="view-title">Sube tu Foto</h2>

    <div v-if="photoSuccess" class="success-message">
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
      <button 
        @click="uploadImage" 
        class="submit-btn"
        :disabled="isLoading"
      >
        <span v-if="!isLoading">Confirmar Subida 📤</span>
        <span v-else>Procesando...</span>
      </button>

      <div v-if="predictionResult" class="results-container">
        <h3>Resultado del análisis:</h3>
        <div class="emotion-results">
          <div 
            v-for="(score, emotion) in predictionResult" 
            :key="emotion"
            class="emotion-row"
          >
            <span class="emotion-label">{{ emotion }}:</span>
            <span class="emotion-value">{{ (score * 100).toFixed(1) }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import apiClient from "../clients/apiClient";

export default {
  name: "Imagen",
  setup() {
    const photoSuccess = ref(false);
    const isDragOver = ref(false);
    const selectedImage = ref(null);
    const fileInput = ref(null);
    const file = ref(null); // Almacenar el objeto File
    const isLoading = ref(false);
    const predictionResult = ref(null);
    const errorMessage = ref(null);

    const triggerFileInput = () => {
      fileInput.value.click();
    };

    const handleFileSelect = (event) => {
      const selectedFile = event.target.files[0];
      if (selectedFile) {
        file.value = selectedFile;
        processFile(selectedFile);
      }
    };

    const handleFileDrop = (event) => {
      isDragOver.value = false;
      const droppedFile = event.dataTransfer.files[0];
      if (droppedFile) {
        file.value = droppedFile;
        processFile(droppedFile);
      }
    };

    const processFile = (fileToProcess) => {
      if (fileToProcess.size > 5 * 1024 * 1024) {
        errorMessage.value = "El archivo es demasiado grande (máximo 5MB)";
        return;
      }

      if (!fileToProcess.type.startsWith("image/")) {
        errorMessage.value = "Por favor selecciona un archivo de imagen válido";
        return;
      }

      errorMessage.value = null;
      const reader = new FileReader();
      reader.onload = (e) => {
        selectedImage.value = e.target.result;
      };
      reader.readAsDataURL(fileToProcess);
    };

    const removeImage = () => {
      selectedImage.value = null;
      file.value = null;
      predictionResult.value = null;
      errorMessage.value = null;
      if (fileInput.value) {
        fileInput.value.value = "";
      }
    };

    const uploadImage = async () => {
      if (!file.value) return;

      isLoading.value = true;
      errorMessage.value = null;
      photoSuccess.value = false;
      predictionResult.value = null;

      try {
        // Verificar salud del API primero
        await apiClient.checkHealth();
        
        // Subir imagen y obtener predicción
        const result = await apiClient.uploadImage(file.value);
        
        photoSuccess.value = true;
        predictionResult.value = result.prediction;
        
        console.log("Predicción recibida:", result);
      } catch (error) {
        errorMessage.value = "Error al procesar la imagen. Intenta nuevamente.";
        console.error("Error:", error);
      } finally {
        isLoading.value = false;
      }
    };

    return {
      photoSuccess,
      isDragOver,
      selectedImage,
      fileInput,
      isLoading,
      predictionResult,
      errorMessage,
      triggerFileInput,
      handleFileSelect,
      handleFileDrop,
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