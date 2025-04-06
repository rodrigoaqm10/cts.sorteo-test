<template>
    <div class="admin-bg">
      <div class="admin-container">
        <header class="panel-header">
          <div class="logo-area">
            <img src="../assets/cts-turismo-logo.png" alt="CTS Turismo" class="brand-logo" />
            <h2>Panel de Administración</h2>
          </div>
          <div class="header-actions">
            <button @click="generarGanador" class="btn">Generar Ganador</button>
            <button @click="logout" class="btn btn-logout">Cerrar Sesión</button>
          </div>
        </header>
  
        <section class="panel-content">
          <div v-if="mensaje" class="alert success">{{ mensaje }}</div>
          <div v-if="error" class="alert error">{{ error }}</div>
  
          <h3>Participantes Verificados</h3>
          <table v-if="verificados.length > 0" class="table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Email</th>
                <th>Teléfono</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in verificados" :key="p.id">
                <td>{{ p.nombre }}</td>
                <td>{{ p.email }}</td>
                <td>{{ p.telefono }}</td>
                <td>
                  <button
                    @click="eliminarParticipante(p.id)"
                    class="btn btn-eliminar"
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else>
            <p>No hay participantes verificados.</p>
          </div>
        </section>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'AdminView',
    data() {
      return {
        mensaje: '',
        error: '',
        verificados: []
      };
    },
    methods: {
      async generarGanador() {
        try {
          const url = 'http://localhost:8000/api/participantes/generar-ganador/';
          const response = await axios.post(url);
          this.mensaje = response.data.mensaje;
          this.error = '';
          this.fetchVerificados();
        } catch (err) {
          this.error = err.response?.data?.error || 'Error al generar el ganador';
          this.mensaje = '';
        }
      },
      async fetchVerificados() {
        try {
          const url = 'http://localhost:8000/api/participantes/verificados/';
          const response = await axios.get(url);
          this.verificados = response.data;
        } catch (err) {
          this.error = err.response?.data?.error || 'Error al obtener los participantes verificados';
        }
      },
      async eliminarParticipante(id) {
        try {
          const url = `http://localhost:8000/api/participantes/eliminar/${id}/`;
          await axios.delete(url);
          this.mensaje = 'Participante eliminado.';
          this.error = '';
          this.fetchVerificados();
        } catch (err) {
          this.error = err.response?.data?.error || 'Error al eliminar el participante';
          this.mensaje = '';
        }
      },
      logout() {
        localStorage.removeItem('adminAuthenticated');
        this.$router.push('/login');
      }
    },
    mounted() {
      this.fetchVerificados();
    }
  };
  </script>
  
  <style scoped>
  .admin-bg {
    min-height: 1vh;
    background: linear-gradient(to bottom right, #f0f4f8, #cce2ff);
    display: flex;
    justify-content: center;
    font-family: sans-serif;
  }
  
  .admin-container {
    width: 100%;
    max-width: 1100px;
    margin: 2rem;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  /* Encabezado */
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f9fafb;
    padding: 1rem 2rem;
    border-bottom: 1px solid #e2e8f0;
    flex-wrap: wrap;
  }
  
  .logo-area {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .brand-logo {
    width: 50px;
  }
  
  .panel-header h2 {
    margin: 0;
    color: #2f855a;
  }
  
  /* Acciones del header */
  .header-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }
  
  .btn {
    background-color: #2f855a;
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 0.6rem 1.2rem;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.3s;
  }
  .btn:hover {
    background-color: #276749;
  }
  .btn-logout,
  .btn-eliminar {
    background-color: #e53e3e;
  }
  
  /* Contenido */
  .panel-content {
    padding: 1.5rem 2rem;
  }
  
  .panel-content h3 {
    color: #2f855a;
    margin-top: 0;
  }
  
  /* Tabla */
  .table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }
  
  .table thead {
    background: #edf2f7;
  }
  
  .table th,
  .table td {
    padding: 0.75rem;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
  }
  
  /* Alertas */
  .alert {
    margin-top: 1rem;
    padding: 10px;
    border-radius: 6px;
    text-align: center;
    font-size: 0.9rem;
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
  