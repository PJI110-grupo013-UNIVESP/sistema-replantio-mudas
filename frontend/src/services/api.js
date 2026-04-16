// frontend/src/services/api.js
// export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const isProduction = window.location.hostname === 'gaiaconsciencia.com.br' || window.location.hostname === 'www.gaiaconsciencia.com.br';

// Se estiver em produção, usa o túnel da API. Se não, usa o localhost.
export const API_URL = isProduction ? "https://api.gaiaconsciencia.com.br/" : 'http://localhost:8000';