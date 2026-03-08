<script setup>
import { onMounted, ref } from 'vue'

const showForm = ref(false)
const loading = ref(true)
const itemEditingId = ref(null)

const newItem = ref({
  species: '',
  batch: '',
  supplier: '',
  amount: 0
})

const mudas = ref([])

const searchItem = async () => {
  try {
    const response = await fetch("http://localhost:8000/mudas")
    if (response.ok) {
      mudas.value = await response.json()
    }
  } catch (error) {
    console.error("Error when searching for Items:", error)
  } finally {
    loading.value = false
  }
}

const saveItem = async () => {
  try {
    const url = itemEditingId.value
      ? `http://localhost:8000/mudas/${itemEditingId.value}`
      : "http://localhost:8000/mudas"

    const method = itemEditingId.value
      ? 'PUT'
      : 'POST'

    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json'
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

const deleteItem = async (id) => {
  if (!confirm("Tem certeza que deseja excluir esta muda do estoque?")) return;

  try {
    const response = await fetch(`http://localhost:8000/mudas/${id}`, { method: 'DELETE' })
    if (response.ok) {
      mudas.value = mudas.value.filter(m => m.id !== id)
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

    <div class="cabecalho-pagina">
      <h2>Gestão de Viveiro e Estoque</h2>
      <button class="btn-primario" @click="showForm ? cancelForm() : showForm = true">
        {{ showForm ? 'Cancelar' : '+ Cadastrar Nova Muda' }}
      </button>
    </div>

    <div class="card" v-if="showForm">
      <h3>{{ itemEditingId ? 'Editar Muda' : 'Cadastrar Nova Muda' }}</h3>
      <form @submit.prevent="saveItem" class="formulario">

        <div class="grupo-input">
          <label>Espécie da Planta</label>
          <input type="text" v-model="newItem.species" required placeholder="Ex: Ipê Roxo">
        </div>

        <div class="grupo-input">
          <label>Código do Lote</label>
          <input type="text" v-model="newItem.batch" required placeholder="Ex: Lote-001">
        </div>

        <div class="grupo-input">
          <label>Fornecedor</label>
          <input type="text" v-model="newItem.supplier" required placeholder="Nome do Fornecedor">
        </div>

        <div class="grupo-input">
          <label>Quantidade Recebida</label>
          <input type="number" v-model="newItem.amount" required min="1">
        </div>

        <div class="acoes-form">
          <button type="submit" class="btn-sucesso">Salvar no Estoque</button>
        </div>
      </form>
    </div>

    <div class="card">
      <h3>Estoque Atual</h3>
      <table class="tabela-mudas">
        <thead>
          <tr>
            <th>ID</th>
            <th>Lote</th>
            <th>Espécie</th>
            <th>Fornecedor</th>
            <th>Quantidade</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="muda in mudas" :key="muda.id">
            <td>#{{ muda.id }}</td>
            <td><strong>{{ muda.batch }}</strong></td>
            <td>{{ muda.species }}</td>
            <td>{{ muda.supplier }}</td>
            <td>{{ muda.amount }} un.</td>
            <td>
              <button class="btn-acao editar" @click="editItem(muda)">Editar</button>
              <button class="btn-acao excluir" @click="deleteItem(muda.id)">Excluir</button>
            </td>
          </tr>
          <tr v-if="mudas.length === 0">
            <td colspan="6" class="texto-vazio">Nenhuma muda cadastrada no estoque.</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<style scoped>
.viveiro-container {
  display: flex;
  flex-direction: column;
  /* gap: 0px; */
}

/* Cabeçalho */
.cabecalho-pagina {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.cabecalho-pagina h2 {
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

.btn-sucesso {
  background-color: #52b788;
  color: white;
  padding: 10px 20px;
  font-size: 1rem;
}

.btn-sucesso:hover {
  background-color: #40916c;
}

.btn-acao {
  padding: 6px 12px;
  margin-right: 5px;
  border-radius: 4px;
  font-size: 0.85rem;
}

.btn-acao.editar {
  background-color: #fca311;
  color: white;
}

.btn-acao.excluir {
  background-color: #e63946;
  color: white;
}

/* Formulário */
.formulario {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-top: 15px;
}

.grupo-input {
  display: flex;
  flex-direction: column;
}

.grupo-input label {
  margin-bottom: 5px;
  color: #4a5568;
  font-weight: 500;
  font-size: 0.9rem;
}

.grupo-input input {
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  outline: none;
}

.grupo-input input:focus {
  border-color: #52b788;
}

.acoes-form {
  grid-column: span 2;
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

/* Tabela */
.tabela-mudas {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.tabela-mudas th,
.tabela-mudas td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.tabela-mudas th {
  background-color: #f8fafc;
  color: #475569;
  font-weight: 600;
}

.texto-vazio {
  text-align: center;
  color: #94a3b8;
  font-style: italic;
  padding: 20px !important;
}
</style>