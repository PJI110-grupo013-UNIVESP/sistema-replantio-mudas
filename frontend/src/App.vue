<script setup>
import { ref } from "vue";
import { RouterLink, RouterView, useRouter } from "vue-router";

const router = useRouter();
const userName = ref("");
const userRole = ref("");

router.afterEach(() => {
  userName.value = localStorage.getItem("userName") || "";
  userRole.value = localStorage.getItem("userRole") || "common";
});

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("userName");
  localStorage.removeItem("userRole");

  router.push("/");
};
</script>

<template>
  <div v-if="$route.meta.hideMenu">
    <RouterView />
  </div>

  <div class="layout-admin" v-else>
    <aside class="sidebar">
      <div class="logo">
        <img src="@/assets/logo-icon.png" alt="Company logo" class="img-logo" />
        <span>Replantio</span>
      </div>
      <nav>
        <RouterLink to="/dashboard" active-class="active">Dashboard</RouterLink>
        <RouterLink to="/viveiro" active-class="active">Viveiro de Mudas</RouterLink>
        <RouterLink to="/replantios" active-class="active">Áreas de Plantio</RouterLink>
        <RouterLink v-if="userRole === 'admin'" to="/usuarios" active-class="active"
          >Usuários</RouterLink
        >
      </nav>
    </aside>

    <div class="main-content">
      <header class="topbar">
        <h2 class="title">Painel de Controle</h2>

        <div class="perfil-usuario">
          <div class="user">{{ userName }}</div>
          <button @click="logout" class="btn-sair">Sair</button>
        </div>
      </header>

      <main class="content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style>
* {
  margin: 0px;
  padding: 0px;
  box-sizing: border-box;
  font-family: "Open Sans", "roboto", sans-serif;
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

.title {
  color: #1b4332;
  margin-bottom: 10px;
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
  /* border-radius: 16px; */
}

.logo {
  padding: 20px;
  font-size: 1.5rem;
  font-weight: bold;
  background-color: #081c15;
  text-align: center;
  color: #74c69d;
  /* border-radius: 16px; */

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
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
nav a.active {
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

.perfil-usuario {
  display: flex;
  align-items: center;
  gap: 15px;
}

.btn-sair {
  background-color: transparent;
  color: #e63946;
  border: 1px solid #e63946;
  padding: 6px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.85rem;
  transition: 0.3s;
}

.btn-sair:hover {
  background-color: #e63946;
  color: white;
}

/* Miolo da Aplicação */
.content {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.img-logo {
  max-width: 100%;
  height: 50px;
  width: auto;
  display: block;
}
</style>
