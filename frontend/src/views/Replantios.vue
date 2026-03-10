<script setup>
import { ref, onMounted } from 'vue'

const replanting = ref([])
const itemAvaliable = ref([])

// Campos do Formulário
const muda_id = ref('')
const area_name = ref('')
const amount = ref('')
const status = ref('Planejado')
const planned_date = ref('')
const estimated_cost = ref('')

const message = ref('')
const loading = ref(false)

// Carrega as plantas do estoque para o Select
const loadMudas = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch('http://localhost:8000/mudas', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      itemAvaliable.value = await response.json()
    }
  } catch (error) {
    console.error("Erro ao carregar mudas:", error)
  }
}


const loadReplanting = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch('http://localhost:8000/replantios', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      replanting.value = await response.json()
    }
  } catch (error) {
    console.error("Erro ao carregar replantios:", error)
  }
}

const registerPlanting = async () => {
  if (!muda_id.value || !area_name.value || !amount.value) return

  loading.value = true
  const token = localStorage.getItem('token')

  try {
    const response = await fetch('http://localhost:8000/replantios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        muda_id: parseInt(muda_id.value),
        area_name: area_name.value,
        amount: parseInt(amount.value),
        status: status.value,
        planned_date: planned_date.value || null,
        estimated_cost: estimated_cost.value ? parseFloat(estimated_cost.value) : null
      })
    })

    if (response.ok) {
      message.value = "Plantio registado com sucesso! Estoque atualizado."

      muda_id.value = ''
      area_name.value = ''
      amount.value = ''
      planned_date.value = ''
      estimated_cost.value = ''

      loadReplanting()
      loadMudas()

      setTimeout(() => message.value = '', 4000)
    } else {
      const err = await response.json()
      alert("Erro: " + (err.detail || "Não foi possível registar o plantio."))
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const formatDate = (data) => {
  if (!data) return '-'
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}


const getNameSpecie = (id) => {
  const muda = itemAvaliable.value.find(m => m.id === id)
  return muda ? `${muda.species} (Lote: ${muda.batch})` : 'Desconhecida'
}

onMounted(() => {
  loadMudas()
  loadReplanting()
})
</script>

<template>
  <div class="replantio-container">
    <h2 class="title">Registo de Replantio de Áreas</h2>
    <p v-if="message" class="alert">{{ message }}</p>

    <div class="card form-card">
      <h3>Novo Plantio</h3>
      <form @submit.prevent="registerPlanting" class="form-grid">
        <div class="input-group">
          <label>Muda (Viveiro)</label>
          <select v-model="muda_id" required>
            <option value="" disabled>Selecione a espécie...</option>
            <option v-for="muda in itemAvaliable" :key="muda.id" :value="muda.id" :disabled="muda.amount <= 0">
              {{ muda.species }} (Estoque: {{ muda.amount }})
            </option>
          </select>
        </div>

        <div class="input-group">
          <label>Área / Setor</label>
          <input type="text" v-model="area_name" placeholder="Ex: Pç. Santa Terezinha" required>
        </div>

        <div class="input-group">
          <label>Quantidade a Plantar</label>
          <input type="number" v-model="amount" min="1" required>
        </div>

        <div class="input-group">
          <label>Data Planeada</label>
          <input type="date" v-model="planned_date">
        </div>

        <div class="input-group">
          <label>Custo Estimado (R$)</label>
          <input type="number" step="0.01" v-model="estimated_cost" placeholder="0.00">
        </div>

        <div class="input-group">
          <label>Status</label>
          <select v-model="status">
            <option value="Planejado">Planejado</option>
            <option value="Em Execução">Em Execução</option>
            <option value="Concluído">Concluído</option>
          </select>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-add" :disabled="loading">
            {{ loading ? 'A Registar...' : 'Registar Plantio' }}
          </button>
        </div>
      </form>
    </div>

    <div class="card">
      <h3>Histórico de Operações</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Data Plan.</th>
            <th>Área</th>
            <th>Espécie (Lote)</th>
            <th>Qtd.</th>
            <th>Custo Prev.</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rep in replanting" :key="rep.id">
            <td>{{ formatDate(rep.planned_date) }}</td>
            <td><strong>{{ rep.area_name }}</strong></td>
            <td>{{ getNameSpecie(rep.muda_id) }}</td>
            <td>{{ rep.amount }}</td>
            <td>{{ rep.estimated_cost ? 'R$ ' + rep.estimated_cost.toFixed(2) : '-' }}</td>
            <td><span class="badge">{{ rep.status }}</span></td>
          </tr>
          <tr v-if="replanting.length === 0">
            <td colspan="6" style="text-align: center;">Nenhum plantio registado ainda.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.replantio-container {
  max-width: 1000px;
  margin: 0 auto;
}

.alert {
  background: #d8f3dc;
  color: #1b4332;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-weight: bold;
  text-align: center;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.input-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}

.input-group input,
.input-group select {
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  outline: none;
}

.input-group input:focus,
.input-group select:focus {
  border-color: #2d6a4f;
}

.form-actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.btn-add {
  background: #2d6a4f;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.2s;
}

.btn-add:hover:not(:disabled) {
  background: #1b4332;
}

.btn-add:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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
  background: #e2e8f0;
  color: #475569;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}
</style>