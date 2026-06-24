// EduInsight AI -- Shared Types

export interface User {
  id: string; full_name: string; email: string;
  roles: string[]; permissions: string[];
  tenant_slug: string; force_password_reset: boolean;
}
export interface AuthTokens { access_token: string; refresh_token: string; user: User; }
export interface Student {
  id: string; student_code: string; full_name: string;
  gender: string; status: string;
  section_name?: string; batch_name?: string;
  overall_risk_score?: number; risk_level?: string;
}
export interface RiskScore {
  student_id: string; overall_risk_score: number;
  academic_risk_score: number; attendance_risk_score: number;
  risk_level: string; contributing_factors: unknown[]; computed_at: string;
}
export interface AIInsight {
  id: string; insight_type: string; insight_text: string;
  confidence_score: number; generated_at: string;
}
export interface Mark {
  id: string; student_enrollment_id: string; student_name?: string;
  marks_obtained: number | null; max_marks: number; is_absent: boolean; is_verified: boolean;
}
export interface AttendanceRecord {
  enrollment_id: string; full_name: string; student_code: string;
  roll_number?: string; status: string | null;
}
export interface AnalyticsOverview {
  total_students: number; school_avg_pct: number; pass_rate: number;
}
export interface PaginatedResult<T> {
  data: T[]; pagination: { page: number; total: number; total_pages: number; has_next: boolean; has_prev: boolean; };
}
export interface Notification {
  id: string; type: string; title: string; body: string; is_read: boolean; created_at: string;
}
