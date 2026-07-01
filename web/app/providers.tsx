'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { state } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = state(() => new QueryClient())
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
}
