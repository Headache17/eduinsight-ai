'use client'
import { useState } from 'react'
import { useAuthStore } from '@/store/authStore'
import { authApi } from '@/lib/api'

export default function LoginPage() {
  const [email, setEmail] = useState('admin@greenwood.edu')
  const [password, setPassword] = useState('Admin@1234')
  const [error, setError] = useState('')
  const { setAuth } = useAuthStore()

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6">EduInsight AI</h1>
        <p className="text-sm mb-4">Demo: admin@greenwood.edu / Admin@1234</p>
        {error && <p className="text-red-500">{error}</p>}
      </div>
    </div>
  )
}
