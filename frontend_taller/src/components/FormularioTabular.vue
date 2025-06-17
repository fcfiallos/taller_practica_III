<template>
  <div class="card">
    <h2>Análisis de Datos de Estudiante</h2>
    <p>Completa el formulario con los datos del estudiante.</p>
    <div class="form-grid">
      <!-- Copia aquí los campos del formulario tabular -->
      <!-- ...campos... -->
      <div class="form-group">
        <label for="age">Edad:</label>
        <input type="number" id="age" v-model.number="studentData.Age" />
      </div>
      <div class="form-group">
        <label for="cgpa">Promedio (CGPA):</label>
        <input
          type="number"
          id="cgpa"
          step="0.01"
          v-model.number="studentData.CGPA"
        />
      </div>
      <div class="form-group">
        <label for="suicidal">Pensamientos Suicidas:</label>
        <select id="suicidal" v-model.number="studentData.Suicidal_Thoughts">
          <option :value="1">Sí</option>
          <option :value="0">No</option>
        </select>
      </div>
      <div class="form-group">
        <label for="family">Historial Familiar:</label>
        <select
          id="family"
          v-model.number="studentData.Family_History_of_Mental_Illness"
        >
          <option :value="1">Sí</option>
          <option :value="0">No</option>
        </select>
      </div>
      <div class="form-group">
        <label for="academic">Presión Académica (1-5):</label>
        <input
          type="number"
          id="academic"
          min="0"
          max="5"
          v-model.number="studentData.Academic_Pressure"
        />
      </div>
      <div class="form-group">
        <label for="financial">Estrés Financiero (1-5):</label>
        <input
          type="number"
          id="financial"
          min="0"
          max="5"
          v-model.number="studentData.Financial_Stress"
        />
      </div>
      <div class="form-group">
        <label for="hours">Horas de Estudio/Trabajo:</label>
        <input
          type="number"
          id="hours"
          v-model.number="studentData.Work_Study_Hours"
        />
      </div>
      <div class="form-group">
        <label for="study_sat">Satisfacción Estudio (1-5):</label>
        <input
          type="number"
          id="study_sat"
          min="0"
          max="5"
          v-model.number="studentData.Study_Satisfaction"
        />
      </div>
      <div class="form-group">
        <label for="diet">Hábitos Alimenticios:</label>
        <select id="diet" v-model.number="studentData.Dietary_Habits">
          <option :value="2">Bueno</option>
          <option :value="1">Moderado</option>
          <option :value="0">Malo</option>
        </select>
      </div>
      <div class="form-group">
        <label for="sleep">Duración del Sueño:</label>
        <select id="sleep" v-model.number="studentData.Sleep_Duration">
          <option :value="3">&gt; 8 horas</option>
          <option :value="2">7-8 horas</option>
          <option :value="1">5-6 horas</option>
          <option :value="0">&lt; 5 horas</option>
        </select>
      </div>
    </div>
    <div v-if="studentError" class="error-message">{{ studentError }}</div>
    <button @click="handleStudentSubmit" :disabled="isStudentLoading">
      {{ isStudentLoading ? "Analizando..." : "Analizar Estudiante" }}
    </button>
    <div v-if="studentResult" class="result">
      <h3>Resultado del Análisis de Estudiante:</h3>
      <ul class="result-list">
        <li>
          <strong>Clasificación:</strong>
          <span
            :class="
              studentResult.clase_predicha === 0
                ? 'sin-depresion'
                : 'con-depresion'
            "
          >
            {{ studentResult.clasificacion }}
          </span>
        </li>
        <li>
          <strong>Clase predicha:</strong>
          {{
            studentResult.clase_predicha === 0
              ? "Sin depresión"
              : "Con depresión"
          }}
        </li>
        <li>
          <strong>Confianza:</strong>
          {{ (studentResult.confianza * 100).toFixed(2) }}%
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { predictStudent } from "@/clients/apiClient";

const studentData = ref({
  Suicidal_Thoughts: 0,
  Academic_Pressure: 3.0,
  Financial_Stress: 3.0,
  Age: 25,
  Dietary_Habits: 1,
  Study_Satisfaction: 3.0,
  Work_Study_Hours: 7.0,
  Family_History_of_Mental_Illness: 0,
  CGPA: 7.5,
  Sleep_Duration: 1,
});
const studentResult = ref(null);
const isStudentLoading = ref(false);
const studentError = ref("");

const handleStudentSubmit = async () => {
  studentError.value = "";
  studentResult.value = null;
  if (
    !studentData.value.Age ||
    studentData.value.Age < 10 ||
    studentData.value.Age > 100
  ) {
    studentError.value = "Por favor, ingresa una edad válida (10-100).";
    return;
  }
  if (
    !studentData.value.CGPA ||
    studentData.value.CGPA < 0 ||
    studentData.value.CGPA > 10
  ) {
    studentError.value = "Por favor, ingresa un CGPA válido (0-10).";
    return;
  }
  isStudentLoading.value = true;
  try {
    const response = await predictStudent(studentData.value);
    studentResult.value = response.data;
  } catch (error) {
    studentError.value =
      "Ocurrió un error al conectar con la API de estudiante.";
  } finally {
    isStudentLoading.value = false;
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
.form-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(250px, 1fr));
  gap: 20px;
}
.form-group {
  display: flex;
  flex-direction: column;
}
.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}
.form-group input,
.form-group select {
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 1rem;
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