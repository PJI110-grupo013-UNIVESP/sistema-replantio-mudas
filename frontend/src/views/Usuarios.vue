<script setup>
import { ref, onMounted } from 'vue'
import { API_URL } from '@/services/api';

const users = ref([])
const email = ref('')
const name = ref('')
const password = ref('')
const role = ref('common')
const message = ref('')
const userRoleLoggedin = ref(localStorage.getItem('userRole'))

const loadUser = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch(`${API_URL}/users`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      users.value = await response.json()
    } else {
      message.value = "Sem permissão para ver utilizadores."
    }
  } catch (error) {
    console.error(error)
  }
}

const createUser = async () => {
  if (!email.value || !password.value) return
  const token = localStorage.getItem('token')

  try {
    const response = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        name: name.value,
        email: email.value,
        password: password.value,
        role: role.value
      })
    })

    if (response.ok) {
      message.value = "Utilizador criado com sucesso!"
      name.value = ''
      email.value = ''
      password.value = ''
      loadUser()
    } else {
      message.value = "Erro ao criar utilizador."
    }
  } catch (error) {
    console.error(error)
  }
}

const deleteUser = async (id) => {
  if (!confirm("Tem certeza que deseja apagar este utilizador do sistema?")) return;

  const token = localStorage.getItem('token')
  try {
    const response = await fetch(`${API_URL}/users/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.ok) {
      message.value = "Utilizador apagado!"
      users.value = users.value.filter(u => u.id !== id)
    } else {
      const err = await response.json()
      message.value = err.detail || "Erro ao apagar."
    }
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadUser()
})
</script>

<template>
  <div v-if="userRoleLoggedin !== 'admin'" class="access-blocked">
    <h2>Acesso Negado</h2>
    <p>Apenas administradores podem aceder a esta área.</p>
  </div>

  <div v-else class="container-users">
    <h2>Gestão de Usuários</h2>
    <p v-if="message" class="alert">{{ message }}</p>

    <div class="card form-card">
      <h3>Novo Usuários</h3>
      <form @submit.prevent="createUser" class="form-line">
        <input type="text" v-model="name" placeholder="Nome Completo" required>
        <input type="email" v-model="email" placeholder="E-mail" required>
        <input type="password" v-model="password" placeholder="Senha" required>
        <select v-model="role">
          <option value="common">Usuário Comum</option>
          <option value="admin">Administrador</option>
        </select>
        <button type="submit" class="btn-add">Adicionar</button>
      </form>
    </div>

    <div class="card">
      <h3>Usuários Registados</h3>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>E-mail</th>
            <th>Nível de Acesso</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>#{{ user.id }}</td>
            <td><strong>{{ user.name }}</strong></td>
            <td>{{ user.email }}</td>
            <td><span :class="'badge ' + user.role">{{ user.role === 'admin' ? 'Administrador' : 'Comum' }}</span></td>
            <td>
              <button class="btn-delete" @click="deleteUser(user.id)">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.container-users {
  max-width: auto;
  margin: 0 auto;
}

.access-blocked {
  text-align: center;
  margin-top: 50px;
  color: #e63946;
}

.alert {
  background: #d8f3dc;
  color: #1b4332;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-weight: bold;
}

.form-line {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.form-line input,
.form-line select {
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  flex: 1;
}

.btn-add {
  background: #2d6a4f;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  text-align: left;
}

.table th {
  background: #f8fafc;
  padding: 12px;
  border-bottom: 2px solid #e2e8f0;
  color: #475569;
}

.table td {
  padding: 12px;
  border-bottom: 1px solid #e2e8f0;
  color: #1e293b;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.badge.admin {
  background: #ffe4e6;
  color: #e11d48;
}

.badge.comum {
  background: #e0f2fe;
  color: #0284c7;
}

.btn-delete {
  background: #e63946;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.btn-delete:hover {
  background: #c1121f;
}
</style>