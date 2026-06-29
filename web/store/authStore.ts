import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: any | null; accessToken: string | null; tenantId: string | null;
  setAuth: (user: any, token: string, tenant: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>()(persist((set) => ({
  user: null, accessToken: null, tenantId: null,
  setAuth: (user, token, tenant) => set({ user, accessToken: token, tenantId: tenant }),
  clearAuth: () => set({ user: null, accessToken: null, tenantId: null }),
}), { name: 'eduinsight-auth' })));
