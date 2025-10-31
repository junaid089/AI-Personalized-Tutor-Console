# API Documentation - AI Personalized Tutor Console

## Base URL
```
http://localhost:8001/api
```

## Authentication
Currently, no authentication is required. The system uses the Emergent LLM key configured in the environment.

---

## Endpoints

### Health Check

#### GET `/api/health`
Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "service": "AI Tutor Console"
}
```

---

## Student Management

### Create Student

#### POST `/api/students`
Create a new student profile.

**Request Body:**
```json
{
  "name": "John Doe",
  "age_group": "10-12",
  "grade_level": "7th Grade",
  "learning_style": "visual",
  "prior_mastery": 0.0,
  "goals": "Master algebra",
  "pacing_pref": "medium",
  "accessibility_needs": "None"
}
```

**Response:**
```json
{
  "id": "uuid-here",
  "name": "John Doe",
  "age_group": "10-12",
  "grade_level": "7th Grade",
  "learning_style": "visual",
  "prior_mastery": 0.0,
  "goals": "Master algebra",
  "pacing_pref": "medium",
  "accessibility_needs": null,
  "created_at": "2025-10-31T07:18:58.051469"
}
```

### Get All Students

#### GET `/api/students`
Retrieve all student profiles.

**Response:**
```json
[
  {
    "id": "uuid-1",
    "name": "John Doe",
    "grade_level": "7th Grade",
    ...
  }
]
```

### Get Single Student

#### GET `/api/students/{student_id}`
Retrieve a specific student profile.

**Response:**
```json
{
  "id": "uuid-here",
  "name": "John Doe",
  ...
}
```

---

## Hint System (Priority 1)

### Generate Hints

#### POST `/api/hints`
Generate 3 tiered progressive hints for a problem.

**Request Body:**
```json
{
  "problem": "Solve for x: 2x + 5 = 15",
  "difficulty": "medium",
  "topic": "Algebra"
}
```

**Response:**
```json
{
  "hints": [
    "This is a linear equation. Think about isolating x...",
    "Subtract 5 from both sides, then divide by 2...",
    "Step 1: 2x + 5 - 5 = 15 - 5 gives 2x = 10. Step 2: Divide by 2..."
  ],
  "problem": "Solve for x: 2x + 5 = 15"
}
```

**Hint Levels:**
- **Hint 1**: Gentle nudge, identifies concept
- **Hint 2**: More specific approach or formula
- **Hint 3**: Step-by-step outline without final answer

### Generate Solution

#### POST `/api/solutions`
Generate complete step-by-step solution with explanation.

**Request Body:**
```json
{
  "problem": "Solve for x: 2x + 5 = 15",
  "topic": "Algebra"
}
```

**Response:**
```json
{
  "steps": [
    "Step 1: Start with the equation 2x + 5 = 15",
    "Step 2: Subtract 5 from both sides...",
    "Step 3: Divide both sides by 2..."
  ],
  "answer": "x = 5",
  "explanation": "To solve a linear equation, isolate the variable..."
}
```

---

## Practice Problems

### Generate Problems

#### POST `/api/problems`
Generate adaptive practice problems.

**Request Body:**
```json
{
  "topic": "Fractions",
  "difficulty": "medium",
  "count": 3
}
```

**Response:**
```json
{
  "problems": [
    {
      "prompt": "Add 2/3 and 1/4",
      "difficulty": "medium",
      "context": "Sarah has 2/3 of a pizza..."
    },
    ...
  ]
}
```

**Difficulty Levels:**
- `easy`: Basic concepts
- `medium`: Standard problems
- `hard`: Advanced applications

---

## Progress Tracking (Priority 2)

### Calculate Progress

#### POST `/api/progress`
Calculate mastery score and generate progress summary.

**Request Body:**
```json
{
  "student_id": "uuid-here",
  "topic": "Algebra",
  "attempts": [
    {"correct": true},
    {"correct": false},
    {"correct": true}
  ],
  "hints_used": [
    ["hint1"],
    ["hint1", "hint2"],
    []
  ]
}
```

**Response:**
```json
{
  "mastery_score": 66.67,
  "summary": {
    "strengths": ["Good understanding of basic equations"],
    "target_areas": ["Need more practice with word problems"],
    "recommendations": ["Practice 5 more problems on applications"],
    "motivational_message": "Great progress! Keep it up!"
  }
}
```

**Mastery Score Calculation:**
- Base score: Percentage of correct attempts × 100
- Penalty: Up to 20% reduction for excessive hint usage
- Range: 0-100

### Get Student Progress

#### GET `/api/progress/{student_id}`
Retrieve all progress records for a student.

**Response:**
```json
[
  {
    "id": "uuid",
    "student_id": "uuid",
    "topic": "Algebra",
    "mastery_score": 75.5,
    "strengths": ["Linear equations"],
    "target_areas": ["Quadratic equations"],
    "recommendations": ["Practice factoring"],
    "last_updated": "2025-10-31T..."
  }
]
```

---

## Lesson Plans (Priority 3)

### Generate Lesson Plan

#### POST `/api/lesson-plans`
Generate comprehensive personalized lesson plan.

**Request Body:**
```json
{
  "student_id": "uuid-here",
  "topic": "Introduction to Calculus",
  "unit_outline": ["Limits", "Derivatives", "Applications"],
  "session_length": 45
}
```

**Response:**
```json
{
  "objectives": [
    "Understand the concept of limits",
    "Calculate basic derivatives",
    "Apply derivatives to real problems"
  ],
  "activities": [
    {
      "title": "Introduction to Limits",
      "description": "Visual demonstration using graphs...",
      "time_minutes": 15
    },
    {
      "title": "Practice Problems",
      "description": "Work through 5 sample problems...",
      "time_minutes": 20
    }
  ],
  "materials": ["Graphing calculator", "Worksheet", "Whiteboard"]
}
```

---

## Diagnostic Assessment (Priority 4)

### Generate Diagnostic

#### POST `/api/diagnostic`
Generate diagnostic assessment to establish baseline.

**Request Body:**
```json
{
  "topic": "Fractions",
  "num_questions": 5
}
```

**Response:**
```json
{
  "questions": [
    {
      "question": "What is 1/2 + 1/4?",
      "options": ["3/4", "2/6", "1/6", "3/8"],
      "correct_answer": "3/4",
      "difficulty": "easy",
      "skill_tested": "Adding fractions with different denominators"
    },
    ...
  ]
}
```

---

## Learning Sessions

### Create Complete Session

#### POST `/api/sessions`
Create a complete learning session with lesson plan and problems.

**Query Parameters:**
- `student_id`: UUID
- `topic`: string
- `unit_outline`: array of strings

**Response:**
```json
{
  "session_id": "uuid",
  "topic": "Algebra",
  "lesson_plan": { ... },
  "practice_problems": [ ... ]
}
```

### Get Student Sessions

#### GET `/api/sessions/{student_id}`
Retrieve all learning sessions for a student.

**Response:**
```json
[
  {
    "id": "uuid",
    "student_id": "uuid",
    "topic": "Algebra",
    "created_at": "2025-10-31T...",
    ...
  }
]
```

---

## Error Responses

All endpoints may return error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Student not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message"
}
```

---

## Rate Limits

Currently no rate limits are enforced. However, the Emergent LLM key has usage limits based on your account balance.

---

## Interactive Documentation

For interactive API testing, visit:
```
http://localhost:8001/docs
```

This provides a Swagger UI interface where you can:
- View all endpoints
- Test requests directly
- See request/response schemas
- Download OpenAPI specification

---

## Code Examples

### Python
```python
import requests

# Create a student
response = requests.post(
    'http://localhost:8001/api/students',
    json={
        'name': 'Alice',
        'grade_level': '8th Grade',
        'learning_style': 'visual'
    }
)
student = response.json()

# Generate hints
hints = requests.post(
    'http://localhost:8001/api/hints',
    json={
        'problem': 'Solve 2x + 5 = 15',
        'difficulty': 'medium',
        'topic': 'Algebra'
    }
).json()
```

### JavaScript
```javascript
// Create a student
const response = await fetch('http://localhost:8001/api/students', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Alice',
    grade_level: '8th Grade',
    learning_style: 'visual'
  })
});
const student = await response.json();

// Generate hints
const hints = await fetch('http://localhost:8001/api/hints', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    problem: 'Solve 2x + 5 = 15',
    difficulty: 'medium',
    topic: 'Algebra'
  })
}).then(r => r.json());
```

### curl
```bash
# Create a student
curl -X POST http://localhost:8001/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "grade_level": "8th Grade",
    "learning_style": "visual"
  }'

# Generate hints
curl -X POST http://localhost:8001/api/hints \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Solve 2x + 5 = 15",
    "difficulty": "medium",
    "topic": "Algebra"
  }'
```

---

## Best Practices

1. **Always validate input**: Ensure topic and problem fields are not empty
2. **Handle async operations**: AI generation can take 2-5 seconds
3. **Store session IDs**: Save student and session IDs for progress tracking
4. **Progressive hint reveal**: Show hints one at a time, not all at once
5. **Cache solutions**: Store generated solutions to reduce API calls
6. **Error handling**: Always implement try-catch for API calls

---

## Support

For API issues or questions:
- Check the [README.md](README.md) troubleshooting section
- Open an issue on GitHub
- Review logs: `tail -f /var/log/supervisor/backend.err.log`
