<script setup>
defineProps({
    show: Boolean,
    title: String,
    message: String,
    type: {
        type: String,
        default: 'info'
    },
    isConfirm: { type: Boolean, default: false }
})

defineEmits(['close', 'confirm'])
</script>

<template>
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-content" :class="type">

            <div class="icon-container">
                <span v-if="type === 'success'">✅</span>
                <span v-else-if="type === 'error'">❌</span>
                <span v-else-if="type === 'warning'">⚠️</span>
                <span v-else>ℹ️</span>
            </div>

            <h3>{{ title }}</h3>
            <p>{{ message }}</p>

            <div class="buttons-container">
                <button v-if="isConfirm" class="btn-cancel" @click="$emit('close')">Cancelar</button>

                <button class="btn-close" @click="isConfirm ? $emit('confirm') : $emit('close')">
                    {{ isConfirm ? 'Sim, Continuar' : 'Entendi' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
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
    z-index: 9999;
}

.modal-content {
    background: white;
    padding: 30px;
    border-radius: 12px;
    width: 90%;
    max-width: 400px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    animation: slideDown 0.3s ease-out;
}

.modal-content.success {
    border-top: 5px solid #10b981;
}

.modal-content.error {
    border-top: 5px solid #ef4444;
}

.modal-content.warning {
    border-top: 5px solid #f59e0b;
}

.modal-content.info {
    border-top: 5px solid #3b82f6;
}

.icon-container {
    font-size: 3rem;
    margin-bottom: 15px;
}

h3 {
    margin: 0 0 10px 0;
    color: #1e293b;
}

p {
    color: #475569;
    margin-bottom: 25px;
    line-height: 1.5;
}

.btn-close {
    background: #f1f5f9;
    color: #334155;
    border: none;
    padding: 10px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    width: 100%;
    transition: background 0.2s;
}

.btn-close:hover {
    background: #e2e8f0;
}

.buttons-container {
    display: flex;
    gap: 10px;
    justify-content: center;
}

.btn-cancel {
    background: #cbd5e1;
    color: #334155;
    border: none;
    padding: 10px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    transition: background 0.2s;
    width: 100%;
}

.btn-cancel:hover {
    background: #94a3b8;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>