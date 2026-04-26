<script setup>
import { ref, onMounted, computed } from 'vue'
import { API_URL } from '@/services/api';
import ModalAviso from '@/components/ModalAviso.vue';


const replanting = ref([])
const itemAvaliable = ref([])
const filterStatus = ref('Todos')
const filterYear = ref('Todos')

const isAdmin = ref(localStorage.getItem('userRole') === 'admin')

// Campos do Formulário
const muda_id = ref('')
const area_name = ref('')
const amount = ref('')
const status = ref('Planejado')
const planned_date = ref('')
const estimated_cost = ref('')

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
    'Tem Certeza?',
    'Deseja excluir este replantio? As mudas voltarão para o estoque.',
    'warning',
    true
  )
}

// const message = ref('')
const loading = ref(false)

const showEditModal = ref(false)
const editData = ref({
  id: '', muda_id: '', area_name: '', amount: '', status: '', planned_date: '', estimated_cost: ''
})



const loadMudas = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await fetch(`${API_URL}/mudas`, {
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
    const response = await fetch(`${API_URL}/replantios`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      replanting.value = await response.json()
      if (availableYears.value.length > 0) {
        filterYear.value = availableYears.value[0]
      }
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
    const response = await fetch(`${API_URL}/replantios`, {
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
      showWarning('Excelente', 'Plantio registado com sucesso! Estoque atualizado.', 'success')

      muda_id.value = ''
      area_name.value = ''
      amount.value = ''
      planned_date.value = ''
      estimated_cost.value = ''

      loadReplanting()
      loadMudas()
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

const deletePlanting = async () => {
  const id = itemToDeleteId.value
  if (!id) return;

  modalConfig.value.show = false

  const token = localStorage.getItem('token')
  try {
    const response = await fetch(`${API_URL}/replantios/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.ok) {
      showWarning('Excelente', 'Replantio excluído com sucesso!', 'success')
      loadReplanting()
      loadMudas()
    } else {
      const err = await response.json()
      if (err.detail == '') {
        showWarning('Erro', 'Não foi possível excluir o replantio.', 'error')
      } else {
        showWarning('Erro', err.detail, 'error')
      }

    }
  } catch (error) {
    console.error("Erro no delete:", error)
  } finally {
    itemToDeleteId.value = null
  }
}

const openEditModal = (rep) => {
  editData.value = { ...rep }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
}

const submitEdit = async () => {
  loading.value = true
  const token = localStorage.getItem('token')

  try {
    const response = await fetch(`${API_URL}/replantios/${editData.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        muda_id: parseInt(editData.value.muda_id),
        area_name: editData.value.area_name,
        amount: parseInt(editData.value.amount),
        status: editData.value.status,
        planned_date: editData.value.planned_date || null,
        estimated_cost: editData.value.estimated_cost ? parseFloat(editData.value.estimated_cost) : null
      })
    })

    if (response.ok) {

      showWarning('Excelente', 'Replantio atualizado! Estoque reajustado automaticamente.', 'success')

      closeEditModal()
      loadReplanting()
      loadMudas()
    } else {
      const err = await response.json()
      alert("Erro ao editar: " + (err.detail || "Verifique se há estoque suficiente."))
    }
  } catch (error) {
    console.error("Erro na edição:", error)
  } finally {
    loading.value = false
  }
}

const sortedReplanting = computed(() => {
  let filteredList = replanting.value
  if (filterStatus.value !== 'Todos') {
    filteredList = filteredList.filter(rep => rep.status === filterStatus.value)
  }

  if (filterYear.value !== 'Todos') {
    filteredList = filteredList.filter(rep => {
      if (!rep.planned_date) return false
      return rep.planned_date.startsWith(filterYear.value)
    })
  }

  return [...filteredList].sort((a, b) => {
    if (!a.planned_date) return 1;
    if (!b.planned_date) return -1;

    return b.planned_date.localeCompare(a.planned_date);
  })
})

const getStatusClass = (status) => {
  if (status === 'Planejado') return 'badge-planejado'
  if (status === 'Em Execução') return 'badge-execucao'
  if (status === 'Concluído') return 'badge-concluido'
  return ''
}

const availableYears = computed(() => {
  const years = new Set()

  replanting.value.forEach(rep => {
    if (rep.planned_date) {
      const year = rep.planned_date.split('-')[0]
      years.add(year)
    }
  })

  return Array.from(years).sort((a, b) => b - a)
})

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
    <!-- <p v-if="message" class="alert">{{ message }}</p> -->

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
          <label>Data Planejada</label>
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
            {{ loading ? 'Registrando...' : 'Registar Plantio' }}
          </button>
        </div>
      </form>
    </div>

    <div class="card">
      <h3>Histórico de Operações</h3>
      <div class="filters-container">
        <div class="filter-years">
          <span class="filter-label">Ano:</span>
          <select v-model="filterYear" class="select-year">
            <option value="Todos">Todos os Anos</option>
            <option v-for="year in availableYears" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>

        <span style="color: #cbd5e1;">|</span>
        <span class="filter-label">Filtrar por Status:</span>
        <button :class="['btn-filter', { active: filterStatus === 'Todos' }]"
          @click="filterStatus = 'Todos'">Todos</button>
        <button :class="['btn-filter', { active: filterStatus === 'Planejado' }]"
          @click="filterStatus = 'Planejado'">Planejado</button>
        <button :class="['btn-filter', { active: filterStatus === 'Em Execução' }]"
          @click="filterStatus = 'Em Execução'">Em Execução</button>
        <button :class="['btn-filter', { active: filterStatus === 'Concluído' }]"
          @click="filterStatus = 'Concluído'">Concluído</button>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>Data Plan.</th>
            <th>Área</th>
            <th>Espécie (Lote)</th>
            <th>Qtd.</th>
            <th>Custo Prev.</th>
            <th>Status</th>
            <th v-if="isAdmin">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rep in sortedReplanting" :key="rep.id">
            <td>{{ formatDate(rep.planned_date) }}</td>
            <td><strong>{{ rep.area_name }}</strong></td>
            <td>{{ getNameSpecie(rep.muda_id) }}</td>
            <td>{{ rep.amount }}</td>
            <td>{{ rep.estimated_cost ? 'R$ ' + rep.estimated_cost.toFixed(2) : '-' }}</td>
            <td><span class="badge" :class="getStatusClass(rep.status)">{{ rep.status }}</span></td>

            <td v-if="isAdmin" class="actions-cell">
              <button @click="openEditModal(rep)" class="btn-act edit">Editar</button>
              <button @click="forDelete(rep.id)" class="btn-act delete">Excluir</button>
            </td>
          </tr>
          <tr v-if="replanting.length === 0">
            <td colspan="7" style="text-align: center;">Nenhum plantio registado ainda.</td>
          </tr>
        </tbody>
      </table>
    </div>


    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content card">
        <h3>Editar Replantio</h3>
        <form @submit.prevent="submitEdit" class="form-grid">
          <div class="input-group">
            <label>Muda (Viveiro)</label>
            <select v-model="editData.muda_id" required>
              <option v-for="muda in itemAvaliable" :key="muda.id" :value="muda.id">
                {{ muda.species }} (Estoque: {{ muda.amount }})
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Área / Setor</label>
            <input type="text" v-model="editData.area_name" required>
          </div>
          <div class="input-group">
            <label>Quantidade a Plantar</label>
            <input type="number" v-model="editData.amount" min="1" required>
          </div>
          <div class="input-group">
            <label>Data Planejada</label>
            <input type="date" v-model="editData.planned_date">
          </div>
          <div class="input-group">
            <label>Custo Estimado (R$)</label>
            <input type="number" step="0.01" v-model="editData.estimated_cost">
          </div>
          <div class="input-group">
            <label>Status</label>
            <select v-model="editData.status">
              <option value="Planejado">Planejado</option>
              <option value="Em Execução">Em Execução</option>
              <option value="Concluído">Concluído</option>
            </select>
          </div>
          <div class="form-actions modal-actions">
            <button type="button" class="btn-cancel" @click="closeEditModal">Cancelar</button>
            <button type="submit" class="btn-add" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <ModalAviso :show="modalConfig.show" :title="modalConfig.title" :message="modalConfig.message"
    :type="modalConfig.type" :isConfirm="modalConfig.isConfirm" @close="modalConfig.show = false"
    @confirm="deletePlanting" />
</template>

<style scoped>
.replantio-container {
  max-width: auto;
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

button {
  cursor: pointer;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  transition: 0.2s;
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

.actions-cell {
  display: flex;
  gap: 8px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 25px;
  border-radius: 10px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-actions {
  gap: 10px;
}

.btn-cancel {
  background: #cbd5e1;
  color: #334155;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.btn-cancel:hover {
  background: #94a3b8;
}

.badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  display: inline-block;
  text-align: center;
  min-width: 90px;
}

.badge-planejado {
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.badge-execucao {
  background: #fef9c3;
  color: #a16207;
  border: 1px solid #fde047;
}

.badge-concluido {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #86efac;
}


.filters-container {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-label {
  font-weight: bold;
  color: #475569;
  margin-right: 5px;
}

.btn-filter {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #475569;
  padding: 6px 14px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-filter:hover {
  background: #e2e8f0;
}

.btn-filter.active {
  background: #2d6a4f;
  color: white;
  border-color: #2d6a4f;
  font-weight: bold;
}

.filter-years {
  display: flex;
  align-items: center;
  gap: 8px;
}

.select-year {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background-color: white;
  color: #475569;
  font-weight: bold;
  cursor: pointer;
  outline: none;
}

.select-year:focus {
  border-color: #2d6a4f;
}
</style>