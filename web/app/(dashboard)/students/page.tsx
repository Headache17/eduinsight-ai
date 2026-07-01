import { useStudents } from '@/lib/hooks'

export default function StudentsPage() {
  const { data, isLoading } = useStudents()
  return (
    <div>
      <h1>Students</h1>
      {isLoading && <p>Loading...</p>}
      <p>{data?.pagination.total ?? 0} students</p>
    </div>
  )
}
