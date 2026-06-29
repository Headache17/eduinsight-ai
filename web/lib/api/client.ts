import axios from 'axios';
import { useAuthStore } from '@/store/authStore';

const api = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL });

api.interceptors.request.use((cfg) => {
  const { accessToken, tenantId } = useAuthStore.getState();
  if (accessToken) cfg.headers['Authorization'] = `Bearer ${accessToken}`;
  if (tenantId) cfg.headers['X-Tenant-ID'] = tenantId;
  return cfg;
});

export default api;
