import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { tokenStore } from '@/lib/api/client'
import type { User } from '@/types'

interface AuthState {
  user: User | null; isAuthenticated: boolean;
  setAuth: (user: User, accessToken: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist((set) => ({
    user: null, isAuthenticated: false,
    setAuth: (user, accessToken) => {
      tokenStore.set(accessToken); set({ user, isAuthenticated: true });
    },
    logout: () => {
      tokenStore.clear(); set({ user: null, isAuthenticated: false });
    },
  }),
  { name: 'eduinsight-auth', partialize: (s) => ({ user: s.user, isAuthenticated: s.isAuthenticated }) }
)
)
