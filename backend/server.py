from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from datetime import datetime

from database import get_db, init_db
from models import Student, LearningSession, PracticeProblem, Progress
from ai_service import AIEducatorService

app = FastAPI(title="AI Personalized Tutor Console")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Initialize AI service
ai_service = AIEducatorService()

# Serve static files
app.mount("/static", StaticFiles(directory="/app/frontend/static"), name="static")

# Pydantic models for requests
class StudentCreate(BaseModel):
    name: str
    age_group: Optional[str] = None
    grade_level: Optional[str] = None
    learning_style: Optional[str] = "mixed"
    prior_mastery: Optional[float] = 0.0
    goals: Optional[str] = None
    pacing_pref: Optional[str] = "medium"
    accessibility_needs: Optional[str] = None

class ProblemRequest(BaseModel):
    topic: str
    difficulty: str
    count: int = 3

class HintRequest(BaseModel):
    problem: str
    difficulty: str
    topic: str

class SolutionRequest(BaseModel):
    problem: str
    topic: str

class LessonPlanRequest(BaseModel):
    student_id: str
    topic: str
    unit_outline: List[str]
    session_length: int = 45

class ProgressRequest(BaseModel):
    student_id: str
    topic: str
    attempts: List[Dict]
    hints_used: List[List[str]]

class DiagnosticRequest(BaseModel):
    topic: str
    num_questions: int = 5

# API Routes

@app.get("/")
def read_root():
    """Serve the main HTML page"""
    return FileResponse("/app/frontend/templates/index.html")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AI Tutor Console"}

# Student Management
@app.post("/api/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student profile"""
    db_student = Student(
        name=student.name,
        age_group=student.age_group,
        grade_level=student.grade_level,
        learning_style=student.learning_style,
        prior_mastery=student.prior_mastery,
        goals=student.goals,
        pacing_pref=student.pacing_pref,
        accessibility_needs=student.accessibility_needs
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/api/students")
def get_students(db: Session = Depends(get_db)):
    """Get all students"""
    students = db.query(Student).all()
    return students

@app.get("/api/students/{student_id}")
def get_student(student_id: str, db: Session = Depends(get_db)):
    """Get a specific student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Hint System (Priority 1)
@app.post("/api/hints")
async def generate_hints(request: HintRequest):
    """Generate 3 tiered hints for a problem"""
    try:
        hints = await ai_service.generate_hints(
            problem=request.problem,
            difficulty=request.difficulty,
            topic=request.topic
        )
        return {
            "hints": hints,
            "problem": request.problem
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/solutions")
async def generate_solution(request: SolutionRequest):
    """Generate step-by-step solution"""
    try:
        solution = await ai_service.generate_solution(
            problem=request.problem,
            topic=request.topic
        )
        return solution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Practice Problems
@app.post("/api/problems")
async def generate_problems(request: ProblemRequest, db: Session = Depends(get_db)):
    """Generate adaptive practice problems"""
    try:
        # Get default student profile if needed
        student_profile = {"grade_level": "General", "learning_style": "mixed"}
        
        problems = await ai_service.generate_practice_problems(
            topic=request.topic,
            difficulty=request.difficulty,
            count=request.count,
            student_profile=student_profile
        )
        return {"problems": problems}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Progress Tracking (Priority 2)
@app.post("/api/progress")
async def calculate_progress(request: ProgressRequest, db: Session = Depends(get_db)):
    """Calculate mastery score and generate progress summary"""
    try:
        # Calculate mastery score
        mastery_score = await ai_service.calculate_mastery_score(
            attempts=request.attempts,
            hints_used=request.hints_used
        )
        
        # Generate progress summary
        summary = await ai_service.generate_progress_summary(
            student_id=request.student_id,
            topic=request.topic,
            mastery_score=mastery_score,
            attempts=request.attempts
        )
        
        # Save progress to database
        progress = Progress(
            student_id=request.student_id,
            topic=request.topic,
            mastery_score=mastery_score,
            strengths=summary.get("strengths", []),
            target_areas=summary.get("target_areas", []),
            recommendations=summary.get("recommendations", [])
        )
        db.add(progress)
        db.commit()
        
        return {
            "mastery_score": mastery_score,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/progress/{student_id}")
def get_student_progress(student_id: str, db: Session = Depends(get_db)):
    """Get student's progress across all topics"""
    progress_records = db.query(Progress).filter(Progress.student_id == student_id).all()
    return progress_records

# Lesson Plans (Priority 3)
@app.post("/api/lesson-plans")
async def generate_lesson_plan(request: LessonPlanRequest, db: Session = Depends(get_db)):
    """Generate comprehensive lesson plan"""
    try:
        # Get student profile
        student = db.query(Student).filter(Student.id == request.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        student_profile = {
            "grade_level": student.grade_level,
            "learning_style": student.learning_style,
            "pacing_pref": student.pacing_pref
        }
        
        lesson_plan = await ai_service.generate_lesson_plan(
            topic=request.topic,
            unit_outline=request.unit_outline,
            student_profile=student_profile,
            session_length=request.session_length
        )
        
        return lesson_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Diagnostic Assessment (Priority 4)
@app.post("/api/diagnostic")
async def generate_diagnostic(request: DiagnosticRequest):
    """Generate diagnostic assessment"""
    try:
        assessment = await ai_service.generate_diagnostic_assessment(
            topic=request.topic,
            num_questions=request.num_questions
        )
        return assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Learning Session Management
@app.post("/api/sessions")
async def create_learning_session(
    student_id: str,
    topic: str,
    unit_outline: List[str],
    db: Session = Depends(get_db)
):
    """Create a complete learning session"""
    try:
        # Get student
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        student_profile = {
            "grade_level": student.grade_level,
            "learning_style": student.learning_style,
            "pacing_pref": student.pacing_pref
        }
        
        # Generate lesson plan
        lesson_plan = await ai_service.generate_lesson_plan(
            topic=topic,
            unit_outline=unit_outline,
            student_profile=student_profile
        )
        
        # Generate practice problems
        problems = await ai_service.generate_practice_problems(
            topic=topic,
            difficulty="medium",
            count=3,
            student_profile=student_profile
        )
        
        # Create session
        session = LearningSession(
            student_id=student_id,
            topic=topic,
            unit_outline=unit_outline,
            lesson_plan=lesson_plan,
            practice_set=problems
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return {
            "session_id": session.id,
            "topic": topic,
            "lesson_plan": lesson_plan,
            "practice_problems": problems
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{student_id}")
def get_student_sessions(student_id: str, db: Session = Depends(get_db)):
    """Get all learning sessions for a student"""
    sessions = db.query(LearningSession).filter(LearningSession.student_id == student_id).all()
    return sessions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
