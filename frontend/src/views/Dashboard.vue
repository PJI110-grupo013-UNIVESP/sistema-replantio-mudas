<script setup>
import { ref, onMounted } from 'vue'

const statusApi = ref('Carregando...')
const totalMudas = ref(0)
const erroConexao = ref(false)

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/status')
    const data = await response.json()

    statusApi.value = data.status
    totalMudas.value = data.Mudas_Cadastradas
  } catch (erro) {
    console.error("Error to load datas:", erro)
    statusApi.value = "Offline"
    erroConexao.value = true
  }
})
</script>

<template>
  <div class="dashboard-container">

    <div class="card">
      <h3>Bem-vindo ao Sistema de Gestão de Replantio!</h3>
      <p>O layout base do painel.</p>
      <p></p>
    </div>

    <div class="card">
      <h3>Visão Geral do Replantio</h3>
      <p>Este é o Dashboard principal</p>
    </div>

    <div class="card">
      <h3>Status do Sistema</h3>
      <p>
        <strong>Servidor: </strong>
        <span :class="{ 'text-error': erroConexao, 'text-ok': !erroConexao }">
          {{ statusApi }}
        </span>
      </p>

      <p v-if="!erroConexao">
        <strong>Mudas em Estoque: </strong> {{ totalMudas }}
      </p>

      <p v-if="erroConexao" class="text-error">
        Não foi possível conectar ao Backend. Verifique se a API está rodando!
      </p>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.text-ok {
  color: #2d6a4f;
  font-weight: bold;
}

.text-error {
  color: #e63946;
  font-weight: bold;
}
</style>