from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import json
from dotenv import load_dotenv

load_dotenv()

class AIEducatorService:
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    def _create_chat(self, system_message: str):
        """Create a new chat instance with Claude"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id="tutor_session",
            system_message=system_message
        ).with_model("anthropic", "claude-3-7-sonnet-20250219")
        return chat
    
    async def generate_hints(self, problem: str, difficulty: str, topic: str):
        """Generate 3 tiered hints for a problem"""
        system_message = """You are an expert educator creating tiered hints for practice problems.
        Generate exactly 3 hints with progressive guidance:
        - Hint 1: Gentle nudge, identifies what concept to use
        - Hint 2: More specific, suggests an approach or formula
        - Hint 3: Step-by-step outline without giving the final answer
        
        Return ONLY valid JSON in this format:
        {
            "hint1": "First gentle hint...",
            "hint2": "More specific hint...",
            "hint3": "Detailed step-by-step outline..."
        }"""
        
        chat = self._create_chat(system_message)
        prompt = f"""Topic: {topic}
Difficulty: {difficulty}
Problem: {problem}

Generate 3 tiered hints in JSON format."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        try:
            # Clean response and parse JSON
            clean_response = response.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith('```'):
                clean_response = clean_response[3:-3].strip()
            
            hints_data = json.loads(clean_response)
            return [
                hints_data.get("hint1", ""),
                hints_data.get("hint2", ""),
                hints_data.get("hint3", "")
            ]
        except json.JSONDecodeError:
            # Fallback to basic hints
            return [
                f"Consider what you know about {topic}",
                f"Think about the {difficulty} level approach",
                "Break the problem into smaller steps"
            ]
    
    async def generate_solution(self, problem: str, topic: str):
        """Generate step-by-step solution"""
        system_message = """You are an expert educator providing clear, step-by-step solutions.
        Break down the solution into numbered steps with clear reasoning.
        Include the final answer at the end.
        
        Return ONLY valid JSON in this format:
        {
            "steps": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
            "answer": "Final answer",
            "explanation": "Brief explanation of key concepts"
        }"""
        
        chat = self._create_chat(system_message)
        prompt = f"""Topic: {topic}
Problem: {problem}

Generate a complete step-by-step solution in JSON format."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        try:
            clean_response = response.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith('```'):
                clean_response = clean_response[3:-3].strip()
            
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return {
                "steps": ["Solution being generated..."],
                "answer": "Calculating...",
                "explanation": "Working on solution"
            }
    
    async def generate_practice_problems(self, topic: str, difficulty: str, count: int, student_profile: dict):
        """Generate adaptive practice problems"""
        system_message = """You are an expert educator creating practice problems.
        Generate problems that are appropriate for the student's level and learning style.
        Include context and clear problem statements.
        
        Return ONLY valid JSON in this format:
        {
            "problems": [
                {
                    "prompt": "Problem statement...",
                    "difficulty": "easy/medium/hard",
                    "context": "Real-world context..."
                }
            ]
        }"""
        
        chat = self._create_chat(system_message)
        prompt = f"""Create {count} practice problems for:
        Topic: {topic}
        Difficulty: {difficulty}
        Student Grade: {student_profile.get('grade_level', 'General')}
        Learning Style: {student_profile.get('learning_style', 'mixed')}
        
        Generate problems in JSON format."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        try:
            clean_response = response.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith('```'):
                clean_response = clean_response[3:-3].strip()
            
            data = json.loads(clean_response)
            return data.get("problems", [])
        except json.JSONDecodeError:
            return []
    
    async def calculate_mastery_score(self, attempts: list, hints_used: list) -> float:
        """Calculate mastery score based on attempts and hints used"""
        if not attempts:
            return 0.0
        
        correct_count = sum(1 for a in attempts if a.get('correct', False))
        total_hints = sum(len(h) for h in hints_used)
        
        # Base score from correctness
        base_score = (correct_count / len(attempts)) * 100
        
        # Penalty for excessive hint usage (max 20% reduction)
        hint_penalty = min(total_hints * 5, 20)
        
        final_score = max(0, base_score - hint_penalty)
        return round(final_score, 2)
    
    async def generate_progress_summary(self, student_id: str, topic: str, mastery_score: float, attempts: list):
        """Generate personalized progress summary and recommendations"""
        system_message = """You are an expert educator providing personalized feedback and recommendations.
        Analyze the student's performance and provide actionable next steps.
        
        Return ONLY valid JSON in this format:
        {
            "strengths": ["Strength 1", "Strength 2"],
            "target_areas": ["Area to improve 1", "Area to improve 2"],
            "recommendations": ["Next step 1", "Next step 2"],
            "motivational_message": "Encouraging message"
        }"""
        
        chat = self._create_chat(system_message)
        prompt = f"""Analyze this student's performance:
        Topic: {topic}
        Mastery Score: {mastery_score}/100
        Total Attempts: {len(attempts)}
        Correct: {sum(1 for a in attempts if a.get('correct', False))}
        
        Generate a progress summary with recommendations in JSON format."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        try:
            clean_response = response.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith('```'):
                clean_response = clean_response[3:-3].strip()
            
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return {
                "strengths": ["Making progress"],
                "target_areas": ["Continue practicing"],
                "recommendations": ["Try more problems"],
                "motivational_message": "Keep up the great work!"
            }
    
    async def generate_lesson_plan(self, topic: str, unit_outline: list, student_profile: dict, session_length: int = 45):
        """Generate comprehensive lesson plan"""
        system_message = """You are an expert curriculum designer creating detailed lesson plans.
        Include measurable objectives, engaging activities, and time estimates.
        
        Return ONLY valid JSON in this format:
        {
            "objectives": ["Objective 1", "Objective 2", "Objective 3"],
            "activities": [
                {
                    "title": "Activity name",
                    "description": "What to do",
                    "time_minutes": 10
                }
            ],
            "materials": ["Material 1", "Material 2"]
        }"""
        
        chat = self._create_chat(system_message)
        prompt = f"""Create a {session_length}-minute lesson plan for:
        Topic: {topic}
        Unit Outline: {', '.join(unit_outline)}
        Student Grade: {student_profile.get('grade_level', 'General')}
        Learning Style: {student_profile.get('learning_style', 'mixed')}
        Pacing: {student_profile.get('pacing_pref', 'medium')}
        
        Generate lesson plan in JSON format."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        try:
            clean_response = response.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith('```'):
                clean_response = clean_response[3:-3].strip()
            
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return {
                "objectives": ["Learn key concepts"],
                "activities": [{"title": "Practice", "description": "Work on problems", "time_minutes": session_length}],
                "materials": ["Notebook", "Pen"]
            }
    
    async def generate_diagnostic_assessment(self, topic: str, num_questions: int = 5):
        """Generate diagnostic quiz to assess baseline mastery"""
        system_message = """You are an expert assessment designer creating diagnostic quizzes.
        Create varied difficulty questions to establish baseline understanding.
        
        Return ONLY valid JSON in this format:
        {
            "questions": [
                {
                    "question": "Question text",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                    "difficulty": "easy/medium/hard",
                    "skill_tested": "Specific skill"
                }
            ]
        }"""
        
        chat = self._create_chat(system_message)
        prompt = f"""Create a {num_questions}-question diagnostic assessment for:
        Topic: {topic}
        
        Include a mix of easy, medium, and hard questions.
        Generate assessment in JSON format."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        try:
            clean_response = response.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith('```'):
                clean_response = clean_response[3:-3].strip()
            
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return {
                "questions": []
            }