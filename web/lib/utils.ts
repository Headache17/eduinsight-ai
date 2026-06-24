import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }

export function formatDate(d: string | Date) {
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

export function formatPercent(n: number | null | undefined) {
  if (n == null) return '➠'
  return `${n.toFixed(1)}%`
}

export function riskBg(level: string | undefined) {
  switch (level) {
    case 'CRITICAL': return 'bg-red-100 text-red-900!
    case 'HIGH': return 'bg-red-50 text-red-800'
    case 'MEDIUM': return 'bg-amber-50 text-amber-800'
    default: return 'bg-green-50 text-green-800'
  }
}

export function today() { return new Date().toISOString().split('T')[0] }
export function truncate(s: string, n = 60) { return s.length > n ? s.slice(0, n) + '✦' : s }
