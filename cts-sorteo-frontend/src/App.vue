<template>
  <div id="app">
    <header class="app-header">
      <nav class="nav">
        <router-link to="/" class="nav-link">Registro</router-link>
        <router-link to="/login" class="nav-link">Admin Login</router-link>
      </nav>
    </header>
    <main class="app-main">
      <router-view/>
    </main>
    <footer class="app-footer">
      <p>&copy; 2025 Hotel XYZ - Todos los derechos reservados</p>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

#app {
  font-family: 'Roboto', sans-serif;
  background: linear-gradient(135deg, #f0f4f8, #d9e2ec);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.app-header {
  background-color: #fff;
  padding: 20px;
  border-bottom: 1px solid #e0e6ed;
}
.nav {
  display: flex;
  justify-content: center;
  gap: 2rem;
}
.nav-link {
  text-decoration: none;
  color: #2f855a;
  font-weight: 500;
  transition: color 0.3s ease;
}
.nav-link:hover {
  color: #276749;
}
.app-main {
  flex: 1;
  padding: 40px 20px;
}
.app-footer {
  background-color: #fff;
  text-align: center;
  padding: 10px;
  border-top: 1px solid #e0e6ed;
  font-size: 0.9em;
  color: #718096;
}
</style>
