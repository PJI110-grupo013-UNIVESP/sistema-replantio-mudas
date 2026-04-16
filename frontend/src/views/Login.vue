form-login
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { API_URL } from "@/services/api";

const router = useRouter();
const email = ref("");
const password = ref("");
const errorLogin = ref(false);
const loading = ref(false);

const userlogin = async () => {
  if (!email.value || !password.value) return;
  loading.value = true;
  errorLogin.value = false;

  try {
    const formData = new URLSearchParams();
    formData.append("username", email.value);
    formData.append("password", password.value);

    const response = await fetch(`${API_URL}/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();

      localStorage.setItem("token", data.access_token);

      const meResponse = await fetch(`${API_URL}/users/me`, {
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      });
      if (meResponse.ok) {
        const meData = await meResponse.json();
        localStorage.setItem("userName", meData.name);
        localStorage.setItem("userRole", meData.role);
      }

      router.push("/dashboard");
    } else {
      errorLogin.value = true;
    }
  } catch (error) {
    console.error("Login communication error:", error);
    errorLogin.value = true;
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="login-container">
    <div class="presentation">
      <div class="content-presentation">
        <h1>Sistema de Replantio de Mudas</h1>
        <p>
          Plataforma inteligente para gestão de viveiros, controle de estoque e monitoramento de
          áreas de plantio ecológico.
        </p>
      </div>
    </div>

    <div class="area-login">
      <div class="card-login">
        <h2>Bem-vindo de volta</h2>
        <p class="subtitle">Insira suas credenciais para acessar o painel</p>

        <form @submit.prevent="userlogin" class="form-login">
          <div class="grup-input">
            <label>E-mail</label>
            <input type="email" v-model="email" placeholder="seu@email.com" required />
          </div>

          <div class="grup-input">
            <label>Senha</label>
            <input type="password" v-model="password" placeholder="••••••••" required />
          </div>

          <!-- <div class="extra-options">
            <label class="remember-me"> <input type="checkbox" /> Lembrar de mim </label>
            <a href="#" class="forgot-passwd">Esqueceu a senha?</a>
          </div> -->

          <p v-if="errorLogin" style="color: #e63946; font-size: 0.85rem; text-align: center; font-weight: bold">
            E-mail ou senha incorretos. Tente novamente.
          </p>

          <button type="submit" class="enter-btn" :disabled="loading">
            {{ loading ? "Entrando ..." : "Entrar no Sistema" }}
          </button>
        </form>

        <!-- <p class="footer-text">Não tem uma conta? <a href="#">Solicite acesso</a></p> -->
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  overflow-y: auto;
}

.presentation {
  flex: 0.9;
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.content-presentation {
  max-width: 100vh;
}

.content-presentation h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #d8f3dc;
}

.content-presentation p {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #b7e4c7;
}

.area-login {
  flex: 1;
  background-color: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.card-login {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 400px;
}

.card-login h2 {
  color: #1e293b;
  margin-bottom: 5px;
}

.subtitle {
  color: #64748b;
  margin-bottom: 30px;
  font-size: 0.9rem;
}

.form-login {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.grup-input {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.grup-input label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #475569;
}

.grup-input input {
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  outline: none;
}

.grup-input input:focus {
  border-color: #52b788;
}

.extra-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.forgot-passwd {
  color: #2d6a4f;
  text-decoration: none;
  font-weight: 600;
}

.enter-btn {
  background-color: #2d6a4f;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.enter-btn:hover {
  background-color: #1b4332;
}

.footer-text {
  margin-top: 20px;
  text-align: center;
  font-size: 0.9rem;
  color: #64748b;
}

.footer-text a {
  color: #2d6a4f;
  font-weight: bold;
  text-decoration: none;
}

/* @media (max-width: 785px) {
  .login-container {
    flex-direction: column;
  }

  .area-login {
    padding: 5px;
  }

  .card-login {
    padding: 20px;
  }
} */
</style>
