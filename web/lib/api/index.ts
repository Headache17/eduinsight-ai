import api from './client';

export const authApi = {
  login: (d: any) => api.post('/v1/auth/login', d),
  logout: () => api.post('/v1/auth/logout'),
};

export const studentsApi = {
  list: (params?: any) => api.get('/v1/students', { params }),
  get: (id: string) => api.get(`/v1/students/${id}`),
};

export const attendanceApi = {
  list: (params?: any) => api.get('/v1/attendance', { params }),
};

export const marksApi = {
  draft: (d: any) => api.post('/v1/marks/draft', d),
};

export const analyticsApi = {
  dashboard: () => api.get('/v1/analytics/dashboard'),
};
