<template>
  <div class="card">
    <h2>Análisis de Texto</h2>
    <p>
      Escribe un texto para analizar si su contenido indica un estado depresivo.
    </p>
    <textarea
      v-model="textInput"
      placeholder="Escribe el texto aquí..."
      rows="6"
    ></textarea>
    <div v-if="textError" class="error-message">{{ textError }}</div>
    <button @click="handleTextSubmit" :disabled="isTextLoading">
      {{ isTextLoading ? "Analizando..." : "Analizar Texto" }}
    </button>
    <div v-if="textResult" class="result">
      <h3>Resultado del Análisis de Texto:</h3>
      <ul class="result-list">
        <li>
          <strong>Texto evaluado:</strong>
          <span>{{ textResult.texto_evaluado }}</span>
        </li>
        <li>
          <strong>Clasificación:</strong>
          <span
            :class="textResult.clase_predicha === 1 ? 'deprimido' : 'normal'"
          >
            {{ textResult.clasificacion }}
          </span>
        </li>
        <li>
          <strong>Confianza Deprimido:</strong>
          {{ (textResult.confianza.deprimido * 100).toFixed(2) }}%
        </li>
        <li>
          <strong>Confianza Normal:</strong>
          {{ (textResult.confianza.normal * 100).toFixed(2) }}%
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { predictText } from "@/clients/apiClient";

const textInput = ref("");
const textResult = ref(null);
const isTextLoading = ref(false);
const textError = ref("");

const handleTextSubmit = async () => {
  textError.value = "";
  textResult.value = null;
  if (!textInput.value.trim()) {
    textError.value = "Por favor, escribe un texto.";
    return;
  }
  isTextLoading.value = true;
  try {
    const response = await predictText(textInput.value);
    textResult.value = response.data;
  } catch (error) {
    textError.value = "Ocurrió un error al conectar con la API de texto.";
  } finally {
    isTextLoading.value = false;
  }
};
</script>

<style scoped>
/* Puedes copiar los estilos de tu Formulario.vue */
.card {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
textarea {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 1rem;
  margin-top: 10px;
}
button {
  display: block;
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
button:hover:not(:disabled) {
  background-color: #36a374;
}
.result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f3f3f3;
  border-radius: 4px;
}
.result-list {
  list-style: none;
  padding: 0;
  margin: 0;
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
</style>