"""
EduInsight AI - Tenant Schema DDL
Returns SQL DDL for creating all 28 tenant-scoped tables.
Each school gets its own PostgreSQL schema: tenant_{uuid_no_dashes}
"""

from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional


def get_tenant_ddl(schema_name: str) -> str:
    """Return complete DDL SQL for a new tenant schema."""
    return f"""
-- Create schema
CREATE SCHEMA IF NOT EXISTS {schema_name};

-- Users and auth
CREATE TABLE IF NOT EXISTS {schema_name}.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    full_name VARCHAR(200) NOT NULL,
    employee_id VARCHAR(100),
    designation VARCHAR(150),
    password_hash VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'INVITED',
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_secret VARCHAR(100),
    force_password_reset BOOLEAN NOT NULL DEFAULT TRUE,
    failed_login_count INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ,
    last_login_at TIMESTAMPTZ,
    last_login_ip INET,
    joining_date DATE,
    created_by UUID,
    updated_by UUID,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS {schema_name}.refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES {schema_name}.users(id),
    token_hash VARCHAR(64) NOT NULL UNIQUE,
    device_info JSONB,
    ip_address INET,
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_at TIMESTAMPTZ,
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS {schema_name}.roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    role_level INTEGER NOT NULL DEFAULT 50,
    is_system_role BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS {schema_name}.permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    scope VARCHAR(50) NOT NULL DEFAULT 'own',
    description TEXT,
    UNIQUE(resource, action, scope)
);

CREATE TABLE IF NOT EXISTS {schema_name}.role_permissions (
    role_id UUID NOT NULL REFERENCES {schema_name}.roles(id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES {schema_name}.permissions(id) ON DELETE CASCADE,
    PRIMARY KEY(role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS {schema_name}.user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES {schema_name}.users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES {schema_name}.roles(id) ON DELETE CASCADE,
    scope_type VARCHAR(50),
    scope_id UUID,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    valid_until DATE,
    assigned_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Academic structure
CREATE TABLE IF NOT EXISTS {schema_name}.academic_years (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(20) NOT NULL,
    label VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT FALSE,
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    locked_by UUID,
    locked_at TIMESTAMPTZ,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS {schema_name}.departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    head_user_id UUID REFERENCES {schema_name}.users(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS {schema_name}.batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    academic_year_id UUID NOT NULL REFERENCES {schema_name}.academic_years(id),
    department_id UUID REFERENCES {schema_name}.departments(id),
    name VARCHAR(50) NOT NULL,
    grade_level VARCHAR(20) NOT NULL,
    class_teacher_id UUID REFERENCES {schema_name}.users(id),
    max_students INTEGER DEFAULT 200,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(academic_year_id, name)
);

CREATE TABLE IF NOT EXISTS {schema_name}.sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id UUID NOT NULL REFERENCES {schema_name}.batches(id),
    name VARCHAR(20) NOT NULL,
    display_name VARCHAR(100),
    max_strength INTEGER NOT NULL DEFAULT 40,
    room_number VARCHAR(20),
    class_teacher_id UUID REFERENCES {schema_name}.users(id),
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(batch_id, name)
);

CREATE TABLE IF NOT EXISTS {schema_name}.subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    department_id UUID REFERENCES {schema_name}.departments(id),
    name VARCHAR(150) NOT NULL,
    code VARCHAR(20) NOT NULL,
    subject_type VARCHAR(50) NOT NULL DEFAULT 'THEORY',
    is_elective BOOLEAN NOT NULL DEFAULT FALSE,
    credit_hours INTEGER,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(code)
);

CREATE TABLE IF NOT EXISTS {schema_name}.subject_teachers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES {schema_name}.users(id),
    subject_id UUID NOT NULL REFERENCES {schema_name}.subjects(id),
    section_id UUID NOT NULL REFERENCES {schema_name}.sections(id),
    academic_year_id UUID NOT NULL REFERENCES {schema_name}.academic_years(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, subject_id, section_id, academic_year_id)
);

-- Students
CREATE TABLE IF NOT EXISTS {schema_name}.students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_code VARCHAR(20) NOT NULL UNIQUE,
    admission_number VARCHAR(100),
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(300) GENERATED ALWAYS AS (first_name || ' ' || COALESCE(middle_name || ' ', '') || last_name) STORED,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(30) NOT NULL,
    blood_group VARCHAR(10),
    category VARCHAR(50),
    mother_tongue VARCHAR(50),
    nationality VARCHAR(50) NOT NULL DEFAULT 'Indian',
    special_needs BOOLEAN NOT NULL DEFAULT FALSE,
    photo_url TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    address_permanent JSONB,
    address_current JSONB,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by UUID,
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS {schema_name}.student_enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES {schema_name}.students(id),
    section_id UUID NOT NULL REFERENCES {schema_name}.sections(id),
    academic_year_id UUID NOT NULL REFERENCES {schema_name}.academic_years(id),
    roll_number VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    leaving_date DATE,
    leaving_reason TEXT,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(student_id, academic_year_id)
);

CREATE TABLE IF NOT EXISTS {schema_name}.guardians (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    occupation VARCHAR(100),
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS {schema_name}.student_guardians (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES {schema_name}.students(id),
    guardian_id UUID NOT NULL REFERENCES {schema_name}.guardians(id),
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    receives_sms BOOLEAN NOT NULL DEFAULT TRUE,
    receives_email BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE(student_id, guardian_id)
);

-- Attendance
CREATE TABLE IF NOT EXISTS {schema_name}.attendance_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_enrollment_id UUID NOT NULL REFERENCES {schema_name}.student_enrollments(id),
    section_id UUID NOT NULL REFERENCES {schema_name}.sections(id),
    academic_year_id UUID NOT NULL REFERENCES {schema_name}.academic_years(id),
    attendance_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    period_number SMALLINT,
    remarks TEXT,
    is_revised BOOLEAN NOT NULL DEFAULT FALSE,
    revised_by UUID REFERENCES {schema_name}.users(id),
    revision_reason TEXT,
    marked_by UUID REFERENCES {schema_name}.users(id),
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by UUID,
    UNIQUE(student_enrollment_id, attendance_date, COALESCE(period_number, -1))
);

-- Exams and marks
CREATE TABLE IF NOT EXISTS {schema_name}.exam_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    weight NUMERIC(5,2) NOT NULL DEFAULT 1.0,
    counts_for_result BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS {schema_name}.exams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    academic_year_id UUID NOT NULL REFERENCES {schema_name}.academic_years(id),
    exam_type_id UUID NOT NULL REFERENCES {schema_name}.exam_types(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    exam_date DATE,
    start_date DATE,
    end_date DATE,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS {schema_name}.exam_subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id UUID NOT NULL REFERENCES {schema_name}.exams(id),
    subject_id UUID NOT NULL REFERENCES {schema_name}.subjects(id),
    section_id UUID NOT NULL REFERENCES {schema_name}.sections(id),
    max_marks NUMERIC(6,2) NOT NULL,
    passing_marks NUMERIC(6,2) NOT NULL,
    grace_marks_allowed NUMERIC(4,2) NOT NULL DEFAULT 0,
    exam_date DATE,
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(exam_id, subject_id, section_id)
);

CREATE TABLE IF NOT EXISTS {schema_name}.marks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_subject_id UUID NOT NULL REFERENCES {schema_name}.exam_subjects(id),
    student_enrollment_id UUID NOT NULL REFERENCES {schema_name}.student_enrollments(id),
    marks_obtained NUMERIC(6,2),
    max_marks NUMERIC(6,2) NOT NULL,
    marks_percentage NUMERIC(5,2) GENERATED ALWAYS AS (
        CASE WHEN marks_obtained IS NOT NULL AND max_marks > 0
             THEN ROUND((marks_obtained / max_marks * 100)::NUMERIC, 2) END
    ) STORED,
    grace_marks NUMERIC(4,2),
    grade VARCHAR(5),
    grade_points NUMERIC(4,2),
    is_absent BOOLEAN NOT NULL DEFAULT FALSE,
    is_withheld BOOLEAN NOT NULL DEFAULT FALSE,
    withheld_reason VARCHAR(100),
    is_practical BOOLEAN NOT NULL DEFAULT FALSE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_by UUID REFERENCES {schema_name}.users(id),
    verified_at TIMESTAMPTZ,
    entered_by UUID REFERENCES {schema_name}.users(id),
    entered_at TIMESTAMPTZ,
    remarks VARCHAR(500),
    revision_number INTEGER NOT NULL DEFAULT 0,
    previous_marks_id UUID,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by UUID,
    UNIQUE(exam_subject_id, student_enrollment_id)
);

-- AI and Risk
CREATE TABLE IF NOT EXISTS {schema_name}.student_risk_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES {schema_name}.students(id),
    academic_year_id UUID NOT NULL REFERENCES {schema_name}.academic_years(id),
    overall_risk_score NUMERIC(5,2) NOT NULL,
    previous_score NUMERIC(5,2),
    academic_risk_score NUMERIC(5,2),
    attendance_risk_score NUMERIC(5,2),
    behavioral_risk_score NUMERIC(5,2),
    risk_level VARCHAR(20) NOT NULL,
    contributing_factors JSONB NOT NULL DEFAULT '[]',
    feature_vector JSONB,
    model_version VARCHAR(50),
    prediction_basis VARCHAR(100),
    computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(student_id, academic_year_id)
);

CREATE TABLE IF NOT EXISTS {schema_name}.ai_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES {schema_name}.students(id),
    insight_type VARCHAR(100) NOT NULL,
    insight_category VARCHAR(50) NOT NULL DEFAULT 'GENERAL',
    insight_text TEXT NOT NULL,
    insight_data JSONB NOT NULL DEFAULT '{}',
    confidence_score NUMERIC(4,3),
    llm_model VARCHAR(100),
    data_fingerprint VARCHAR(64),
    is_reviewed BOOLEAN NOT NULL DEFAULT FALSE,
    is_dismissed BOOLEAN NOT NULL DEFAULT FALSE,
    dismissed_by UUID,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Interventions
CREATE TABLE IF NOT EXISTS {schema_name}.interventions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES {schema_name}.students(id),
    academic_year_id UUID NOT NULL REFERENCES {schema_name}.academic_years(id),
    assigned_to UUID NOT NULL REFERENCES {schema_name}.users(id),
    triggered_by_insight_id UUID REFERENCES {schema_name}.ai_insights(id),
    intervention_type VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    status VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    due_date DATE,
    completed_date DATE,
    outcome VARCHAR(50),
    outcome_notes TEXT,
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by UUID,
    deleted_at TIMESTAMPTZ
);

-- Notifications
CREATE TABLE IF NOT EXISTS {schema_name}.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES {schema_name}.users(id),
    type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    action_url TEXT,
    action_label VARCHAR(100),
    resource_type VARCHAR(50),
    resource_id UUID,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    is_dismissed BOOLEAN NOT NULL DEFAULT FALSE,
    read_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Audit log
CREATE TABLE IF NOT EXISTS {schema_name}.audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id UUID,
    actor_email VARCHAR(255),
    actor_role VARCHAR(50),
    action VARCHAR(200) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    ip_address INET,
    user_agent VARCHAR(500),
    session_id VARCHAR(64),
    http_status INTEGER,
    request_id VARCHAR(64),
    failure_reason TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'SUCCESS',
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Materialized view for analytics
CREATE MATERIALIZED VIEW IF NOT EXISTS {schema_name}.mv_section_performance AS
SELECT
    es.exam_id,
    es.section_id,
    es.subject_id,
    COUNT(DISTINCT se.id)                                               AS total_students,
    COUNT(m.id) FILTER (WHERE m.is_absent)                             AS absent_count,
    COUNT(m.id) FILTER (WHERE m.marks_percentage >= 33 AND NOT m.is_absent) AS passed_count,
    ROUND(AVG(m.marks_percentage)::NUMERIC, 2)                         AS avg_percentage,
    MAX(m.marks_obtained)                                              AS highest_marks,
    MIN(m.marks_obtained) FILTER (WHERE NOT m.is_absent)               AS lowest_marks,
    ROUND(STDDEV(m.marks_percentage)::NUMERIC, 2)                      AS std_deviation,
    NOW()                                                              AS refreshed_at
FROM {schema_name}.exam_subjects es
JOIN {schema_name}.student_enrollments se ON se.section_id = es.section_id AND se.status = 'ACTIVE'
LEFT JOIN {schema_name}.marks m ON m.exam_subject_id = es.id AND m.student_enrollment_id = se.id AND m.is_verified
WHERE es.deleted_at IS NULL
GROUP BY es.exam_id, es.section_id, es.subject_id
WITH NO DATA;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_{schema_name}_users_email ON {schema_name}.users(email);
CREATE INDEX IF NOT EXISTS idx_{schema_name}_students_code ON {schema_name}.students(student_code);
CREATE INDEX IF NOT EXISTS idx_{schema_name}_attendance_date ON {schema_name}.attendance_records(attendance_date, section_id);
CREATE INDEX IF NOT EXISTS idx_{schema_name}_marks_enrollment ON {schema_name}.marks(student_enrollment_id);
CREATE INDEX IF NOT EXISTS idx_{schema_name}_risk_scores_level ON {schema_name}.student_risk_scores(risk_level, overall_risk_score DESC);
"""


def create_tenant_schema(schema_name: str) -> list[str]:
    """Split DDL into individual statements for execution."""
    ddl = get_tenant_ddl(schema_name)
    statements = [s.strip() for s in ddl.split(';') if s.strip()]
    return statements
