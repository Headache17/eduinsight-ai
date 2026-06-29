import { useQuery } from '@tanstack/react-query';
import { studentsApi, analyticsApi } from '@/lib/api';

export const useStudents = (params?: any) =>
  useQuery({ queryKey: ['students', params], queryFn: () => studentsApi.list(params).then(r => r.data) });

export const useStudent = (id: string) =>
  useQuery({ queryKey: ['student', id], queryFn: () => studentsApi.get(id).then(r => r.data) });

export const useDashboard = () =>
  useQuery({ queryKey: ['dashboard'], queryFn: () => analyticsApi.dashboard().then(r => r.data) });
