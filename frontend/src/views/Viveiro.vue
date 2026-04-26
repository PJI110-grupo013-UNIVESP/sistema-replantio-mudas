<script setup>
import { onMounted, ref } from 'vue'
import { API_URL } from '@/services/api';
import ModalAviso from '@/components/ModalAviso.vue';


const showForm = ref(false)
const loading = ref(true)
const itemEditingId = ref(null)

const isAdmin = ref(localStorage.getItem('userRole') === 'admin')

const itemToDeleteId = ref(null)
const modalConfig = ref({
  show: false,
  title: '',
  message: '',
  type: 'info',
  isConfirm: false
})

const showWarning = (title, message, type = 'info', isConfirm = false) => {
  modalConfig.value = { show: true, title, message, type, isConfirm }
}

const forDelete = (id) => {
  itemToDeleteId.value = id
  showWarning(
    'Cuidado!',
    'Tem certeza que deseja excluir esta muda do estoque?',
    'warning',
    true
  )
}

const newItem = ref({
  species: '',
  batch: '',
  supplier: '',
  amount: 0
})

const mudas = ref([])

const searchItem = async () => {

  try {
    const token = localStorage.getItem('token')

    const response = await fetch(`${API_URL}/mudas`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (response.ok) {
      mudas.value = await response.json()
    }
  } catch (error) {
    console.error("Error when searching for Items:", error)
  } finally {
    loading.value = false
  }
}

const saveEditItem = async () => {
  try {
    const token = localStorage.getItem('token')

    const url = itemEditingId.value
      ? `${API_URL}/mudas/${itemEditingId.value}`
      : `${API_URL}/mudas`

    const method = itemEditingId.value
      ? 'PUT'
      : 'POST'

    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(newItem.value)
    })

    if (response.ok) {
      const itemCreated = await response.json()

      if (itemEditingId.value) {
        const index = mudas.value.findIndex(m => m.id === itemEditingId.value)
        mudas.value[index] = itemCreated
      } else {
        mudas.value.push(itemCreated)
      }

      newItem.value = {
        species: '',
        batch: '',
        supplier: '',
        amount: 0
      }
      showForm.value = false
      showWarning('Excelente!', 'Muda salva no estoque com sucesso.', 'success')
    }
  } catch (error) {
    console.error("Error to save an Item:", error)
    alert("Unable to save. Check your connection to the server.")
  }
}

const editItem = (muda) => {
  newItem.value = { ...muda }
  itemEditingId.value = muda.id
  showForm.value = true
}

const deleteItem = async () => {
  const id = itemToDeleteId.value
  if (!id) return;

  modalConfig.value.show = false

  try {
    const token = localStorage.getItem('token')

    const response = await fetch(`${API_URL}/mudas/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    })
    if (response.ok) {
      mudas.value = mudas.value.filter(m => m.id !== id)
      showWarning('Feito!', 'Muda removida do estoque.', 'success')
    }
  } catch (error) {
    console.error("Erro ao excluir:", error)
  }
}

// Limpa tudo ao cancelar
const cancelForm = () => {
  newItem.value = { species: '', batch: '', supplier: '', amount: 0 }
  itemEditingId.value = null
  showForm.value = false
}

onMounted(() => {
  searchItem()
})

</script>

<template>
  <div class="viveiro-container">

    <div class="page-header">
      <h2>Gestão de Viveiro e Estoque</h2>
      <button v-if="isAdmin" class="btn-primario" @click="showForm ? cancelForm() : showForm = true">
        {{ showForm ? 'Cancelar' : '+ Cadastrar Nova Muda' }}
      </button>
    </div>

    <div class="card" v-if="showForm">
      <h3>{{ itemEditingId ? 'Editar Muda' : 'Cadastrar Nova Muda' }}</h3>
      <form @submit.prevent="saveEditItem" class="form">

        <div class="input-group">
          <label>Espécie da Planta</label>
          <input type="text" v-model="newItem.species" required placeholder="Ex: Ipê Roxo">
        </div>

        <div class="input-group">
          <label>Código do Lote</label>
          <input type="text" v-model="newItem.batch" required placeholder="Ex: Lote-001">
        </div>

        <div class="input-group">
          <label>Fornecedor</label>
          <input type="text" v-model="newItem.supplier" required placeholder="Nome do Fornecedor">
        </div>

        <div class="input-group">
          <label>Quantidade Recebida</label>
          <input type="number" v-model="newItem.amount" required min="1">
        </div>

        <div class="act-form">
          <button type="submit" class="btn-success">Salvar no Estoque</button>
        </div>
      </form>
    </div>

    <div class="card">
      <h3>Estoque Atual</h3>
      <table class="mudas-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Lote</th>
            <th>Espécie</th>
            <th>Fornecedor</th>
            <th>Quantidade</th>
            <th v-if="isAdmin">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="muda in mudas" :key="muda.id">
            <td>#{{ muda.id }}</td>
            <td><strong>{{ muda.batch }}</strong></td>
            <td>{{ muda.species }}</td>
            <td>{{ muda.supplier }}</td>
            <td>{{ muda.amount }} un.</td>
            <td v-if="isAdmin">
              <button class="btn-act edit" @click="editItem(muda)">Editar</button>
              <button class="btn-act delete" @click="forDelete(muda.id)">Excluir</button>
            </td>
          </tr>
          <tr v-if="loading">
            <td colspan="6" class="blank-text">Carregando estoque... ⏳</td>
          </tr>
          <tr v-if="mudas.length === 0">
            <td colspan="6" class="blank-text">Nenhuma muda cadastrada no estoque.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <ModalAviso :show="modalConfig.show" :title="modalConfig.title" :message="modalConfig.message"
    :type="modalConfig.type" :isConfirm="modalConfig.isConfirm" @close="modalConfig.show = false"
    @confirm="deleteItem" />
</template>

<style scoped>
.viveiro-container {
  display: flex;
  flex-direction: column;
  /* gap: 0px; */
}

/* Cabeçalho */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.page-header h2 {
  color: #1b4332;
}

/* Botões */
button {
  cursor: pointer;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  transition: 0.2s;
}

.btn-primario {
  background-color: #2d6a4f;
  color: white;
  padding: 10px 20px;
}

.btn-primario:hover {
  background-color: #1b4332;
}

.btn-success {
  background-color: #52b788;
  color: white;
  padding: 10px 20px;
  font-size: 1rem;
}

.btn-success:hover {
  background-color: #40916c;
}

.btn-act {
  padding: 6px 12px;
  margin-right: 5px;
  border-radius: 4px;
  font-size: 0.85rem;
}

.btn-act.edit {
  background-color: #fca311;
  color: white;
}

.btn-act.delete {
  background-color: #e63946;
  color: white;
}

/* Formulário */
.form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-top: 15px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  margin-bottom: 5px;
  color: #4a5568;
  font-weight: 500;
  font-size: 0.9rem;
}

.input-group input {
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  outline: none;
}

.input-group input:focus {
  border-color: #52b788;
}

.act-form {
  grid-column: span 2;
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

/* Tabela */
.mudas-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.mudas-table th,
.mudas-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.mudas-table th {
  background-color: #f8fafc;
  color: #475569;
  font-weight: 600;
}

.blank-text {
  text-align: center;
  color: #94a3b8;
  font-style: italic;
  padding: 20px !important;
}
</style>