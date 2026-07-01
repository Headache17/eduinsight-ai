import { useStudent } from '@/lib/hooks'

export default function StudentDetailPage({ params }: { params: { id: string } }) {
  const { data, isLoading } = useStudent(params.id)
  if (isLoading) return <p>Loading...</p>
  return <div><h1>{display?.full_name}</h1></div>
}
