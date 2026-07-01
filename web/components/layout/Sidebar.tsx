'use client'
import Link from 'next/link'

const navItems = [
  { href: '/', label: 'Dashboard' },
  { href: '/students', label: 'Students' },
  { href: '/attendance', label: 'Attendance' },
  { href: '/marks', label: 'Marks' },
  { href: '/analytics', label: 'Analytics' },
]

export function Sidebar() {
  return (
    <nav className="w-64 bg-gray-900 text-white h-screen p-4">
      <h2 className="text-lg font-bold mb-6">EduInsight AI</h2>
      {navItems.map((item) => (
        <Link key={item.href} href={item.href} className="block py-2 px-4 rounded hover:bg-gray-700">
          {item.label}
        </Link>
      ))}
    </nav>
  )
}