<template>
  <div class="app-container">
    <!-- Animated background -->
    <div class="bg-particles">
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
      <div class="particle"></div>
    </div>

    <!-- Header -->
    <header class="header">
      <div class="nav-container">
        <div class="logo">✨ FeelMirror 😃</div>
        <div class="nav-buttons">
          <button
            class="nav-btn"
            :class="{ active: currentView === 'form' }"
            @click="currentView = 'form'"
          >
            📝 Formulario
          </button>
          <button
            class="nav-btn"
            :class="{ active: currentView === 'photo' }"
            @click="currentView = 'photo'"
          >
            📸 Subir Foto
          </button>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="main-content">
      <Formulario v-if="currentView === 'form'" />
      <Imagen v-if="currentView === 'photo'" />
    </main>
  </div>
</template>

<script>
import { ref } from "vue";
import Formulario from "./components/Formulario.vue";
import Imagen from "./components/Imagen.vue";

export default {
  name: "App",
  components: {
    Formulario,
    Imagen,
  },
  setup() {
    const currentView = ref("form");

    return {
      currentView,
    };
  },
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* Animated background particles */
.bg-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

.particle:nth-child(1) {
  width: 80px;
  height: 80px;
  left: 10%;
  animation-delay: 0s;
}
.particle:nth-child(2) {
  width: 60px;
  height: 60px;
  left: 20%;
  animation-delay: 2s;
}
.particle:nth-child(3) {
  width: 100px;
  height: 100px;
  left: 35%;
  animation-delay: 4s;
}
.particle:nth-child(4) {
  width: 40px;
  height: 40px;
  left: 70%;
  animation-delay: 1s;
}
.particle:nth-child(5) {
  width: 120px;
  height: 120px;
  left: 85%;
  animation-delay: 3s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

/* Header */
.header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 0;
  position: relative;
  z-index: 10;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

.nav-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.nav-btn.active {
  background: linear-gradient(45deg, #ff6b6b, #ffd93d);
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
}

/* Main content */
.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  position: relative;
  z-index: 5;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
    padding: 0 1rem;
  }

  .main-content {
    padding: 1rem;
  }
}
</style>