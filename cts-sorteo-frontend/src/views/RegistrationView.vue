<template>
  <div class="app-bg">
    <div class="center-container">
      <div class="logo-block">
        <img src="../assets/cts-turismo-logo.png" alt="CTS Turismo" class="brand-logo" />
        <h1>CTS Turismo</h1>
        <p class="subtitle">
          ¡Participa en nuestro sorteo!<br />
          Gana una estadía romántica de 2 noches con todo pagado.
        </p>
      </div>

      <div class="form-card">
        <h2>Registro de Participante</h2>
        <form @submit.prevent="registrarParticipante">
          <div class="form-group">
            <label for="nombre">Nombre</label>
            <input
              id="nombre"
              v-model="nombre"
              type="text"
              placeholder="Ingresa tu nombre"
              required
            />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="tu@email.com"
              required
            />
          </div>
          <div class="form-group">
            <label for="telefono">Teléfono</label>
            <input
              id="telefono"
              v-model="telefono"
              type="text"
              placeholder="Número de teléfono"
              required
            />
          </div>
          <button type="submit" class="btn">Registrar</button>
        </form>
        <p v-if="mensaje" class="alert success">{{ mensaje }}</p>
        <p v-if="error" class="alert error">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'RegistrationView',
  data() {
    return {
      nombre: '',
      email: '',
      telefono: '',
      mensaje: '',
      error: ''
    };
  },
  methods: {
    async registrarParticipante() {
      try {
        const url = 'http://localhost:8000/api/participantes/registro-completo/';
        const response = await axios.post(url, {
          nombre: this.nombre,
          email: this.email,
          telefono: this.telefono
        });
        this.mensaje = response.data.mensaje;
        this.error = '';
      } catch (err) {
        this.error = err.response?.data?.error || 'Error en el registro';
        this.mensaje = '';
      }
    }
  }
};
</script>

<style scoped>
/* Fondo con gradiente sutil */
.app-bg {
  min-height: 1vh;
  background: linear-gradient(to bottom right, #f0f4f8, #cce2ff);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: sans-serif;
}

/* Contenedor centrado */
.center-container {
  width: 100%;
  max-width: 420px;
  margin: 2rem;
  text-align: center;
}

/* Bloque de logo y texto inicial */
.logo-block {
  margin-bottom: 1.5rem;
}

.brand-logo {
  width: 80px;
  margin-bottom: 0.5rem;
}

.subtitle {
  margin: 0.5rem 0;
  font-size: 1rem;
  color: #444;
}

/* Tarjeta de formulario */
.form-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.form-card h2 {
  text-align: center;
  margin-bottom: 1rem;
  color: #2f855a;
  font-weight: 600;
}

/* Grupo de formulario */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-size: 0.9rem;
  color: #4a5568;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  border-color: #2f855a;
  outline: none;
}

/* Botón */
.btn {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #2f855a;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 8px;
  transition: 0.3s;
}
.btn:hover {
  background-color: #276749;
}

/* Alertas */
.alert {
  margin-top: 1rem;
  padding: 10px;
  border-radius: 6px;
  font-size: 0.9rem;
  text-align: center;
}

.alert.success {
  background-color: #d4edda;
  color: #155724;
}
.alert.error {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
