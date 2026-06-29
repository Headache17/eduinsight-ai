export interface User {
  id: string; full_name: string; email: string;
  roles: string[]; permissions: string[];
  tenant_slug: string; force_password_reset: boolean;
}
export interface Student { id: string; student_code: string; full_name: string; risk_level?: string; }
export interface PaginatedResult<T> { data: T[]; pagination: { total: number; }; }
