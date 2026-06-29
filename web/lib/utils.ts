import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) { return twMerge(clsx( inputs)); }
export const formatDate = (d: string) => new Date(d).toLocaleDateString('en-IN');
export const formatPct = (n: number) => `${n.toFixed(1)}%`;
export const getRiskColor = (l: string) => ({ CRITICAL:'red', HIGH:'orange', MEDIUM:'yellow', LOW:'green' }[l] || 'gray');
