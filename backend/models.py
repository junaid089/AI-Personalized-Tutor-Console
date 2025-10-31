from sqlalchemy import Column, String, Integer, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    age_group = Column(String)
    grade_level = Column(String)
    learning_style = Column(String)  # visual/auditory/kinesthetic/reading
    prior_mastery = Column(Float, default=0.0)
    goals = Column(Text)
    pacing_pref = Column(String)  # slow/medium/fast
    accessibility_needs = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sessions = relationship("LearningSession", back_populates="student")
    progress_records = relationship("Progress", back_populates="student")

class LearningSession(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("students.id"))
    topic = Column(String, nullable=False)
    unit_outline = Column(JSON)
    lesson_plan = Column(JSON)
    practice_set = Column(JSON)
    explanations = Column(JSON)
    progress_summary = Column(JSON)
    assessment = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="sessions")
    problems = relationship("PracticeProblem", back_populates="session")

class PracticeProblem(Base):
    __tablename__ = "practice_problems"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("learning_sessions.id"))
    prompt_text = Column(Text, nullable=False)
    difficulty = Column(String)  # easy/medium/hard
    hints = Column(JSON)  # Array of 3 hints
    solution_steps = Column(JSON)  # Step-by-step solution
    answer = Column(Text)
    mastery_indicator = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("LearningSession", back_populates="problems")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("students.id"))
    topic = Column(String, nullable=False)
    mastery_score = Column(Float, default=0.0)  # 0-100
    strengths = Column(JSON)
    target_areas = Column(JSON)
    recommendations = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="progress_records")