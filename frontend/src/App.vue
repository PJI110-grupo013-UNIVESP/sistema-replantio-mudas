<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div class="layout-admin">
    <aside class="sidebar">
      <div class="logo">🌱 Replantio</div>
      <nav>
        <RouterLink to="/" active-class="ativo">Dashboard</RouterLink>
        <RouterLink to="/viveiro" active-class="ativo">Viveiro de Mudas</RouterLink>
        <a href="#">Áreas de Plantio</a>
        <a href="#">Usuários</a>
      </nav>
    </aside>

    <div class="main-content">
      <header class="topbar">
        <h2>Visão Geral</h2>
        <div class="user">Olá, Guest</div>
      </header>

      <main class="content">

        <RouterView />
      </main>
    </div>
  </div>
</template>

<style>
* {
  margin: 1;
  padding: 1;
  box-sizing: border-box;
  font-family: 'Open Sans', 'roboto', sans-serif;
}

.card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(45, 106, 79, 0.1);
  border-top: 4px solid #52b788;
  margin-bottom: 20px;
}

.card h3 {
  color: #1b4332;
  margin-bottom: 10px;
}

.card p {
  color: #4a5568;
  line-height: 1.5;
}
</style>

<style scoped>
.layout-admin {
  display: flex;
  height: 100vh;
  background-color: #f2f7f4;
}


.sidebar {
  width: 250px;
  background-color: #1b4332;
  color: white;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
}

.logo {
  padding: 20px;
  font-size: 1.5rem;
  font-weight: bold;
  background-color: #081c15;
  text-align: center;
  color: #74c69d;
  border-radius: 16px;
}

nav {
  display: flex;
  flex-direction: column;
  padding-top: 20px;
}

nav a {
  color: #b7e4c7;
  text-decoration: none;
  padding: 15px 20px;
  transition: 0.3s;
  border-left: 4px solid transparent;
}

nav a:hover,
nav a.ativo {
  background-color: #2d6a4f;
  border-left: 4px solid #52b788;
  color: white;
  border-radius: 16px;
}

/* Estilos da Parte Direita */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Barra Superior */
.topbar {
  background-color: white;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  color: #1b4332;
}

.topbar h2 {
  color: #2d6a4f;
}

.user {
  font-weight: bold;
  color: #2d6a4f;
  background-color: #d8f3dc;
  padding: 8px 16px;
  border-radius: 20px;
}

/* Miolo da Aplicação */
.content {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}
</style>
