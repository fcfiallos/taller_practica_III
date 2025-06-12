<template>
  <div class="view-container">
    <h2 class="view-title">Cuéntanos cómo te sientes</h2>

    <div v-if="formSuccess" class="success-message">
      ¡Datos guardados exitosamente! ✅
    </div>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label class="form-label">Género</label>
        <select class="form-input" v-model="formData.genero" required>
          <option disabled value="">Selecciona tu género</option>
          <option value="hombre">Hombre</option>
          <option value="mujer">Mujer</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Edad</label>
        <input
          type="number"
          class="form-input"
          v-model="formData.edad"
          min="0"
          required
        />
      </div>

      <div class="form-group">
        <label class="form-label">Presión académica (1-5)</label>
        <input
          type="number"
          class="form-input"
          v-model="formData.presionAcademica"
          min="1"
          max="5"
          required
        />
      </div>

      <div class="form-group">
        <label class="form-label">Satisfacción con el estudio (1-5)</label>
        <input
          type="number"
          class="form-input"
          v-model="formData.satisfaccionEstudio"
          min="1"
          max="5"
          required
        />
      </div>

      <div class="form-group">
        <label class="form-label">Horas de sueño</label>
        <input
          type="number"
          class="form-input"
          v-model="formData.horasSueno"
          min="0"
          required
        />
      </div>

      <div class="form-group">
        <label class="form-label">Hábitos dietéticos</label>
        <select
          class="form-input"
          v-model="formData.habitosDieteticos"
          required
        >
          <option disabled value="">Selecciona una opción</option>
          <option value="saludable">Saludable</option>
          <option value="moderado">Moderado</option>
          <option value="no_saludable">No saludable</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Estrés financiero (1-5)</label>
        <input
          type="number"
          class="form-input"
          v-model="formData.estresFinanciero"
          min="1"
          max="5"
          required
        />
      </div>

      <button type="submit" class="submit-btn">Enviar Datos 🚀</button>
    </form>
  </div>
</template>

<script>
import { ref, reactive } from "vue";

export default {
  name: "Formulario",
  setup() {
    const formSuccess = ref(false);

    const formData = reactive({
      genero: "",
      edad: "",
      presionAcademica: "",
      satisfaccionEstudio: "",
      horasSueno: "",
      habitosDieteticos: "",
      estresFinanciero: "",
    });

    const submitForm = () => {
      // Simular envío del formulario
      console.log("Datos del formulario:", formData);
      formSuccess.value = true;

      // Limpiar el formulario después de 2 segundos
      setTimeout(() => {
        Object.keys(formData).forEach((key) => (formData[key] = ""));
        formSuccess.value = false;
      }, 2000);
    };

    return {
      formData,
      formSuccess,
      submitForm,
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

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #555;
}

.form-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.submit-btn {
  width: 100%;
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