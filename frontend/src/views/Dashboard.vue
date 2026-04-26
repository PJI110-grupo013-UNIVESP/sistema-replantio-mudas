<script setup>
import { ref, onMounted, computed } from 'vue'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, LineElement, PointElement, Filler } from 'chart.js'
import { Bar, Doughnut, Line } from 'vue-chartjs'
import { API_URL } from '@/services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, LineElement, PointElement, Filler)

const mudas = ref([])
const replanting = ref([])
const loading = ref(true)
const filterYear = ref('Todos')

// --- BUSCAR DADOS NA API ---
const loadData = async () => {
  const token = localStorage.getItem('token')
  const headers = { 'Authorization': `Bearer ${token}` }

  try {
    const [resMudas, resReplantios] = await Promise.all([
      fetch(`${API_URL}/mudas`, { headers }),
      fetch(`${API_URL}/replantios`, { headers })
    ])

    if (resMudas.ok) mudas.value = await resMudas.json()
    if (resReplantios.ok) {
      replanting.value = await resReplantios.json()
      if (availableYears.value.length > 0) {
        filterYear.value = availableYears.value[0]
      }
    }
  } catch (error) {
    console.error("Erro ao carregar dados do Dashboard:", error)
  } finally {
    loading.value = false
  }
}

const sortedReplanting = computed(() => {
  return [...filteredReplanting.value].sort((a, b) => {
    if (!a.planned_date) return 1;
    if (!b.planned_date) return -1;

    return b.planned_date.localeCompare(a.planned_date);
  })
})

const availableYears = computed(() => {
  const years = new Set()
  replanting.value.forEach(rep => {
    if (rep.planned_date) {
      years.add(rep.planned_date.split('-')[0])
    }
  })
  return Array.from(years).sort((a, b) => b - a)
})

const filteredReplanting = computed(() => {
  if (filterYear.value === 'Todos') return replanting.value

  return replanting.value.filter(rep => {
    if (!rep.planned_date) return false
    return rep.planned_date.startsWith(filterYear.value)
  })
})

// --- MATEMÁTICA PARA OS CARTÕES DE RESUMO ---
const totalInventory = computed(() => {
  return mudas.value.reduce((total, muda) => total + muda.amount, 0)
})

const totalPlanted = computed(() => {
  return filteredReplanting.value.reduce((total, rep) => total + rep.amount, 0)
})

const totalCost = computed(() => {
  return filteredReplanting.value.reduce((total, rep) => total + (rep.estimated_cost || 0), 0)
})



// --- DADOS PARA O GRÁFICO DE PIZZA (ESTOQUE) ---
const chartStockData = computed(() => {
  const grouped = {}
  mudas.value.forEach(m => {
    grouped[m.species] = (grouped[m.species] || 0) + m.amount
  })

  return {
    labels: Object.keys(grouped),
    datasets: [{
      backgroundColor: ['#1b4332', '#2d6a4f', '#40916c', '#52b788', '#74c69d'],
      data: Object.values(grouped)
    }]
  }
})

// --- DADOS PARA O GRÁFICO DE BARRAS (ÁREAS) ---
const chartDataAreas = computed(() => {
  const grouped = {}
  filteredReplanting.value.forEach(r => {
    grouped[r.area_name] = (grouped[r.area_name] || 0) + r.amount
  })

  return {
    labels: Object.keys(grouped),
    datasets: [{
      label: 'Mudas Plantadas',
      backgroundColor: '#2d6a4f',
      data: Object.values(grouped)
    }]
  }
})

// --- DADOS PARA O GRÁFICO DE PIZZA (STATUS) ---
const chartDataStatus = computed(() => {
  const grouped = {}
  filteredReplanting.value.forEach(r => {
    grouped[r.status] = (grouped[r.status] || 0) + 1
  })

  const colors = Object.keys(grouped).map(status => {
    if (status === 'Concluído') return '#10b981'
    if (status === 'Em Execução') return '#3b82f6'
    return '#f59e0b'
  })

  return {
    labels: Object.keys(grouped),
    datasets: [{
      backgroundColor: colors,
      data: Object.values(grouped)
    }]
  }
})

// --- DADOS PARA O GRÁFICO DE LINHA ---
const chartDataTime = computed(() => {
  const grouped = {}
  const withDate = filteredReplanting.value
    .filter(r => r.planned_date)
    .sort((a, b) => new Date(a.planned_date) - new Date(b.planned_date))

  const uniqueDates = [...new Set(withDate.map(r => r.planned_date))]

  const dateDone = withDate
    .filter(r => r.status === 'Concluído')
    .map(r => new Date(r.planned_date).getTime())

  const lastDateDone = dateDone.length > 0 ? Math.max(...dateDone) : null

  let accumuPlanned = 0
  let accumuDone = 0

  const dataPlanned = []
  const dataDone = []

  uniqueDates.forEach(date => {
    const plantTheDay = withDate.filter(r => r.planned_date === date)
    const totalDay = plantTheDay.reduce((sum, r) => sum + r.amount, 0)

    const doneDay = plantTheDay
      .filter(r => r.status === 'Concluído')
      .reduce((sum, r) => sum + r.amount, 0)

    accumuPlanned += totalDay
    accumuDone += doneDay

    dataPlanned.push(accumuPlanned)
    // dataDone.push(accumuDone)
    const actualTime = new Date(date).getTime()

    if (lastDateDone !== null && actualTime > lastDateDone) {
      dataDone.push(null)
    } else {
      dataDone.push(accumuDone)
    }
  })
  return {
    labels: uniqueDates.map(formatDate),
    datasets: [
      {
        label: 'Avanço Realizado (Concluídos)',
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.2)',
        data: dataDone,
        fill: true,
        tension: 0.4,
        spanGaps: false
      },
      {
        label: 'Curva Base (Total Planejado)',
        borderColor: '#64748b',
        borderDash: [5, 5],
        backgroundColor: 'transparent',
        data: dataPlanned,
        fill: false,
        tension: 0.4
      }
    ]
  }
  // withDate.forEach(r => {
  //   grouped[r.planned_date] = (grouped[r.planned_date] || 0) + r.amount
  // })

  // return {
  //   labels: Object.keys(grouped).map(formatDate),
  //   datasets: [{
  //     label: 'Volume de Plantio ao Longo do Tempo',
  //     borderColor: '#0284c7',
  //     backgroundColor: 'rgba(2, 132, 199, 0.2)',
  //     data: Object.values(grouped),
  //     fill: true,
  //     tension: 0.4
  //   }]
  // }  
})

// --- DADOS PARA A TABELA DE RECENTES ---
// const recentActivities = computed(() => {
//   return [...replanting.value].reverse().slice(0, 5)
// })


const getSpeciesName = (id) => {
  const muda = mudas.value.find(m => m.id === id)
  return muda ? muda.species : `Muda #${id}`
}

const formatDate = (data) => {
  if (!data) return '-'
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20
      }
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  },
  scales: {
    y: {
      ticks: {
        precision: 0,
      },
      beginAtZero: true,
      title: {
        display: true,
        // text: 'Quantidade de Mudas Acumuladas'
      }
    }
  }
}

// const chartOptions = {
//   responsive: true,
//   maintainAspectRatio: false,
//   scales: {
//     y: {
//       ticks: {
//         precision: 0,
//       }
//     }
//   }
// }

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="dashboard-container">
    <div class="header-container">
      <h2 class="title">Visão Geral do Sistema</h2>

      <div v-if="!loading" class="filter-year">
        <span class="filter-label">Analisar Ano:</span>
        <select v-model="filterYear" class="select-year">
          <option value="Todos">Histórico Completo</option>
          <option v-for="year in availableYears" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">A carregar dados do campo...</div>
    <div v-else>
      <div class="summary-cards">
        <div class="card summary-card">
          <h3>Mudas no Viveiro</h3>
          <p class="number green-highlight">{{ totalInventory }}</p>
        </div>
        <div class="card summary-card">
          <h3>Mudas Plantadas</h3>
          <p class="number blue-highlight">{{ totalPlanted }}</p>
        </div>
        <div class="card summary-card">
          <h3>Custo Est. Replantios</h3>
          <p class="number orange-highlight">R$ {{ totalCost.toFixed(2) }}</p>
        </div>
      </div>

      <div class="charts">
        <div class="card chart-graphic">
          <h3>Evolução do Cronograma</h3>
          <div class="chart-wrapper-graphic">
            <Line :data="chartDataTime" :options="chartOptions" v-if="chartDataTime.labels.length > 0" />
            <p v-else class="no-data">Registre plantios com datas para ver a evolução.</p>
          </div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="card chart-card">
          <h3>Status das Áreas</h3>
          <div class="chart-wrapper">
            <Doughnut :data="chartDataStatus" :options="chartOptions" v-if="replanting.length > 0" />
            <p v-else class="no-data">Nenhum status registado.</p>
          </div>
        </div>

        <div class="card chart-card">
          <h3>Estoque por Espécie</h3>
          <div class="chart-wrapper">
            <Doughnut :data="chartStockData" :options="chartOptions" v-if="mudas.length > 0" />
            <p v-else class="no-data">Sem dados no viveiro.</p>
          </div>
        </div>
      </div>

      <div class="card chart-graphic">
        <h3>Plantio por Área / Setor</h3>
        <div class="chart-wrapper-graphic">
          <Bar :data="chartDataAreas" :options="{ ...chartOptions, plugins: { legend: { display: false } } }"
            v-if="replanting.length > 0" />
          <p v-else class="no-data">Nenhum plantio registado.</p>
        </div>
      </div>

      <div class="card recent-activity">
        <h3>Últimas Movimentações</h3>
        <table class="table">
          <thead>
            <tr>
              <th>Data</th>
              <th>Área de Destino</th>
              <th>Espécie Plantada</th>
              <th>Quantidade</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="activity in sortedReplanting" :key="activity.id">
              <td>{{ formatDate(activity.planned_date) }}</td>
              <td><strong>{{ activity.area_name }}</strong></td>
              <td>{{ getSpeciesName(activity.muda_id) }}</td>
              <td>{{ activity.amount }}</td>
              <td><span :class="['badge', activity.status.replace(' ', '-').toLowerCase()]">{{ activity.status }}</span>
              </td>
            </tr>
            <tr v-if="sortedReplanting.length === 0">
              <td colspan="5" style="text-align: center;" class="no-data">Nenhuma movimentação recente.</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  max-width: auto;
  margin: 0 auto;
  padding-bottom: 40px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.title {
  margin-bottom: 0;
  color: #1e293b;
}

.loading {
  text-align: center;
  margin-top: 50px;
  color: #64748b;
  font-size: 1.2rem;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 15px;
}

.summary-card {
  text-align: center;
  padding: 30px;
}

.summary-card h3 {
  color: #64748b;
  font-size: 0.9rem;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.number {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0;
}

.green-highlight {
  color: #2d6a4f;
}

.blue-highlight {
  color: #0284c7;
}

.orange-highlight {
  color: #ea580c;
}

.chart-graphic {
  padding: 20px;
  display: flexbox;
  flex-direction: column;
  align-items: center;
  min-height: 500px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-card h3 {
  color: #1e293b;
  margin-bottom: 20px;
  font-size: 1.1rem;
  border-bottom: 2px solid #f1f5f9;
  padding-bottom: 10px;
  width: 100%;
  text-align: center;
}

.chart-wrapper {
  position: relative;
  height: 400px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-wrapper-graphic {
  position: relative;
  height: 500px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.no-data {
  color: #94a3b8;
  font-style: italic;
}

.recent-activity {
  padding: 20px;
}

.recent-activity h3 {
  color: #1e293b;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.95rem;
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
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
}

.badge.planned {
  background: #fef3c7;
  color: #d97706;
}

.badge.em-execução {
  background: #dbeafe;
  color: #2563eb;
}

.badge.concluído {
  background: #d1fae5;
  color: #059669;
}

.filter-year {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  padding: 8px 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-label {
  font-weight: bold;
  color: #475569;
}

.select-year {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background-color: #f8fafc;
  color: #1e293b;
  font-weight: bold;
  cursor: pointer;
  outline: none;
  transition: 0.2s;
}

.select-year:focus {
  border-color: #2d6a4f;
  box-shadow: 0 0 0 2px rgba(45, 106, 79, 0.2);
}
</style>