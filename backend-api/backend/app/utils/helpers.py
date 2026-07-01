"""EduInsight AI — Utility Helpers"""
from typing import Tuple, Optional

GRADE_SCHEMAS={"CBSE":[(91,"A1",4.0),(81,"A2",3.8),(71,"B1",3.0),(61,"B2",2.8),(51,"C1",2.0),(41,"C2",1.8),(33,"D",1.0),(0,"F",0.0)]}

def compute_grade(pct, schema="CBSE"):
    schema_def = GRADE_SCHEMAS.get(schema, GRADE_SCHEMAS["CBSE"])
    for thresh, grade, pts in schema_def:
        if pct >= thresh: return grade, pts
    return "F", 0.0

def get_schema_for_board(board): return GRADE_SCHEMAS.get(board, "CBSE")

def generate_student_code(year, count): return f"STU-{year}-{count:04d}"

def paginate(page, page_size): return (page-1)*page_size

def offset(page, page_size): return (page-1)*page_size
