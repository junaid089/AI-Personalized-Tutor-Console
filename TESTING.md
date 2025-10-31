# Testing Guide - AI Personalized Tutor Console

## Manual Testing Checklist

### ✅ Backend API Testing

#### 1. Health Check
```bash
curl http://localhost:8001/api/health
# Expected: {"status":"ok","service":"AI Tutor Console"}
```

#### 2. Student Management
```bash
# Create student
curl -X POST http://localhost:8001/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Student",
    "grade_level": "9th Grade",
    "learning_style": "visual",
    "pacing_pref": "fast"
  }'
# Expected: Returns student object with ID

# List students
curl http://localhost:8001/api/students
# Expected: Array of students

# Get specific student (replace UUID)
curl http://localhost:8001/api/students/{student-id}
# Expected: Student object
```

#### 3. Hint System (Priority 1)
```bash
# Generate hints
curl -X POST http://localhost:8001/api/hints \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Calculate the area of a circle with radius 5",
    "difficulty": "medium",
    "topic": "Geometry"
  }'
# Expected: Object with 3 hints array

# Generate solution
curl -X POST http://localhost:8001/api/solutions \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Calculate the area of a circle with radius 5",
    "topic": "Geometry"
  }'
# Expected: Object with steps, answer, explanation
```

#### 4. Practice Problems
```bash
curl -X POST http://localhost:8001/api/problems \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Algebra",
    "difficulty": "easy",
    "count": 2
  }'
# Expected: Object with problems array
```

#### 5. Progress Tracking (Priority 2)
```bash
curl -X POST http://localhost:8001/api/progress \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "your-student-id",
    "topic": "Algebra",
    "attempts": [{"correct": true}, {"correct": false}],
    "hints_used": [[], ["hint1"]]
  }'
# Expected: mastery_score and summary object

# Get progress
curl http://localhost:8001/api/progress/{student-id}
# Expected: Array of progress records
```

#### 6. Lesson Plans (Priority 3)
```bash
curl -X POST http://localhost:8001/api/lesson-plans \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "your-student-id",
    "topic": "Introduction to Physics",
    "unit_outline": ["Newton Laws", "Forces", "Motion"],
    "session_length": 45
  }'
# Expected: Lesson plan with objectives, activities, materials
```

#### 7. Diagnostic Assessment (Priority 4)
```bash
curl -X POST http://localhost:8001/api/diagnostic \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Basic Arithmetic",
    "num_questions": 3
  }'
# Expected: Object with questions array
```

---

### ✅ Frontend UI Testing

#### 1. Access Application
1. Open browser: `http://localhost:8001`
2. Verify page loads with navigation sidebar
3. Check for "🎓 AI Personalized Tutor Console" header

#### 2. Student Profiles Section
1. Click "👤 Student Profiles" in sidebar
2. Click "+ Add New Student" button
3. Fill form:
   - Name: "John Doe"
   - Grade: "10th Grade"
   - Learning Style: "Visual"
   - Pacing: "Medium"
4. Click "Save Student"
5. Verify student appears in list
6. Check student card shows correct information

#### 3. Practice Problems Section
1. Click "📝 Practice Problems"
2. Enter topic: "Algebra"
3. Select difficulty: "Medium"
4. Set count: 3
5. Click "Generate Problems"
6. Wait for problems to load (3-5 seconds)
7. Verify 3 problems appear

#### 4. Hint System Testing
For each generated problem:
1. Click "💡 Hint 1" - verify hint appears in yellow box
2. Click "💡 Hint 2" - verify second hint appears
3. Click "💡 Hint 3" - verify third hint appears
4. Verify hints are progressively more detailed
5. Click "✓ Show Solution"
6. Verify solution appears with:
   - Numbered steps
   - Final answer
   - Explanation

#### 5. Progress Tracking
1. Click "📊 Progress Tracking"
2. Select student from dropdown
3. Click "Load Progress"
4. Verify progress cards show:
   - Mastery score (0-100)
   - Topic name
   - Strengths list
   - Target areas list
   - Recommendations list

#### 6. Lesson Plans
1. Click "📚 Lesson Plans"
2. Select student
3. Enter topic: "Introduction to Calculus"
4. Enter outline: "Limits, Derivatives, Integrals"
5. Set duration: 45 minutes
6. Click "Generate Lesson Plan"
7. Verify lesson plan displays:
   - Learning objectives
   - Activities with time estimates
   - Materials needed

#### 7. Diagnostic Assessment
1. Click "🧪 Diagnostic"
2. Enter topic: "Fractions"
3. Set questions: 5
4. Click "Generate Assessment"
5. Verify questions appear
6. Click answer options
7. Verify feedback shows correct/incorrect
8. Check all questions have:
   - Question text
   - Multiple choice options
   - Skill tested label
   - Difficulty label

---

## Performance Testing

### Response Time Benchmarks

| Endpoint | Expected Time | Test Command |
|----------|---------------|--------------|
| `/api/health` | < 100ms | `time curl http://localhost:8001/api/health` |
| `/api/students` | < 200ms | `time curl http://localhost:8001/api/students` |
| `/api/hints` | 2-5 seconds | `time curl -X POST http://localhost:8001/api/hints ...` |
| `/api/solutions` | 3-6 seconds | `time curl -X POST http://localhost:8001/api/solutions ...` |
| `/api/problems` | 3-7 seconds | `time curl -X POST http://localhost:8001/api/problems ...` |
| `/api/lesson-plans` | 4-8 seconds | `time curl -X POST http://localhost:8001/api/lesson-plans ...` |

**Note**: AI generation endpoints are slower due to Claude API calls.

---

## Load Testing

### Simple Load Test
```bash
# Test 10 concurrent requests
for i in {1..10}; do
  curl -X POST http://localhost:8001/api/students \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Student $i\", \"grade_level\": \"8th Grade\"}" &
done
wait

# Verify all created
curl http://localhost:8001/api/students | python3 -c "import sys, json; print(len(json.load(sys.stdin)))"
```

---

## Error Handling Testing

### Test Invalid Inputs
```bash
# Missing required field
curl -X POST http://localhost:8001/api/students \
  -H "Content-Type: application/json" \
  -d '{}'
# Expected: 422 Validation Error

# Invalid student ID
curl http://localhost:8001/api/students/invalid-uuid
# Expected: 404 Not Found

# Empty topic
curl -X POST http://localhost:8001/api/problems \
  -H "Content-Type: application/json" \
  -d '{"topic": "", "difficulty": "medium", "count": 3}'
# Expected: Error or empty problems array
```

---

## Database Testing

### Verify Database Persistence
```bash
# Create a student
STUDENT=$(curl -s -X POST http://localhost:8001/api/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Persistence Test", "grade_level": "5th Grade"}')

STUDENT_ID=$(echo $STUDENT | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

# Restart backend
sudo supervisorctl restart backend
sleep 3

# Verify student still exists
curl http://localhost:8001/api/students/$STUDENT_ID
# Expected: Student object returned
```

### Database Query Test
```bash
# Connect to PostgreSQL
sudo -u postgres psql tutor_db -c "SELECT COUNT(*) FROM students;"
sudo -u postgres psql tutor_db -c "SELECT name, grade_level FROM students LIMIT 5;"
```

---

## Integration Testing

### Complete User Flow Test
```bash
#!/bin/bash

echo "=== AI Tutor Console Integration Test ==="

# 1. Create student
echo "1. Creating student..."
STUDENT=$(curl -s -X POST http://localhost:8001/api/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Integration Test", "grade_level": "9th Grade", "learning_style": "visual"}')
STUDENT_ID=$(echo $STUDENT | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "   Student ID: $STUDENT_ID"

# 2. Generate problems
echo "2. Generating practice problems..."
PROBLEMS=$(curl -s -X POST http://localhost:8001/api/problems \
  -H "Content-Type: application/json" \
  -d '{"topic": "Algebra", "difficulty": "medium", "count": 2}')
echo "   Problems generated: $(echo $PROBLEMS | python3 -c "import sys, json; print(len(json.load(sys.stdin)['problems']))")"

# 3. Generate hints
echo "3. Generating hints..."
HINTS=$(curl -s -X POST http://localhost:8001/api/hints \
  -H "Content-Type: application/json" \
  -d '{"problem": "Solve 2x + 5 = 15", "difficulty": "medium", "topic": "Algebra"}')
echo "   Hints count: $(echo $HINTS | python3 -c "import sys, json; print(len(json.load(sys.stdin)['hints']))")"

# 4. Generate solution
echo "4. Generating solution..."
SOLUTION=$(curl -s -X POST http://localhost:8001/api/solutions \
  -H "Content-Type: application/json" \
  -d '{"problem": "Solve 2x + 5 = 15", "topic": "Algebra"}')
echo "   Solution steps: $(echo $SOLUTION | python3 -c "import sys, json; print(len(json.load(sys.stdin)['steps']))")"

# 5. Record progress
echo "5. Recording progress..."
PROGRESS=$(curl -s -X POST http://localhost:8001/api/progress \
  -H "Content-Type: application/json" \
  -d "{\"student_id\": \"$STUDENT_ID\", \"topic\": \"Algebra\", \"attempts\": [{\"correct\": true}, {\"correct\": true}], \"hints_used\": [[], [\"hint1\"]]}")
echo "   Mastery score: $(echo $PROGRESS | python3 -c "import sys, json; print(json.load(sys.stdin)['mastery_score'])")"

# 6. Generate lesson plan
echo "6. Generating lesson plan..."
LESSON=$(curl -s -X POST http://localhost:8001/api/lesson-plans \
  -H "Content-Type: application/json" \
  -d "{\"student_id\": \"$STUDENT_ID\", \"topic\": \"Algebra Basics\", \"unit_outline\": [\"Variables\", \"Equations\"], \"session_length\": 30}")
echo "   Objectives count: $(echo $LESSON | python3 -c "import sys, json; print(len(json.load(sys.stdin)['objectives']))")"

# 7. Get progress
echo "7. Retrieving progress..."
PROGRESS_LIST=$(curl -s http://localhost:8001/api/progress/$STUDENT_ID)
echo "   Progress records: $(echo $PROGRESS_LIST | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")"

echo "=== Integration Test Complete ==="
```

Save as `test_integration.sh`, make executable with `chmod +x test_integration.sh`, and run with `./test_integration.sh`

---

## Browser Testing

### Cross-Browser Compatibility
Test in:
- ✅ Chrome/Chromium (Latest)
- ✅ Firefox (Latest)
- ✅ Safari (Latest)
- ✅ Edge (Latest)

### Mobile Responsive Testing
Test on:
- 📱 iPhone (Safari)
- 📱 Android (Chrome)
- 📱 Tablet devices

### Browser Console Checks
1. Open Developer Tools (F12)
2. Check Console for errors
3. Check Network tab for failed requests
4. Check Application/Storage for proper data handling

---

## Automated Testing (Future Enhancement)

### Python Unit Tests (To be implemented)
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_student():
    response = client.post("/api/students", json={
        "name": "Test Student",
        "grade_level": "8th Grade"
    })
    assert response.status_code == 200
    assert "id" in response.json()
```

### JavaScript Frontend Tests (To be implemented)
```javascript
// tests/frontend.test.js
describe('Student Management', () => {
  it('should create a new student', async () => {
    const response = await fetch('/api/students', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Test', grade_level: '5th' })
    });
    expect(response.ok).toBe(true);
  });
});
```

---

## Test Results Log

Document your test results:

```
Test Date: YYYY-MM-DD
Tester: Your Name
Environment: Development/Production

✅ Backend Health: PASS
✅ Student CRUD: PASS
✅ Hint Generation: PASS (avg 3.2s)
✅ Solution Generation: PASS (avg 4.1s)
✅ Progress Tracking: PASS
✅ Lesson Plans: PASS (avg 5.3s)
✅ Diagnostic: PASS
✅ UI Navigation: PASS
✅ Mobile Responsive: PASS
❌ Feature X: FAIL - Reason

Notes:
- All core features working
- Response times within acceptable range
- Minor UI glitch on mobile (non-blocking)
```

---

## Continuous Testing

### Daily Smoke Tests
```bash
# Run every morning
curl http://localhost:8001/api/health && echo "✅ API is up"
curl http://localhost:8001/ | grep "AI Personalized Tutor" && echo "✅ Frontend is up"
```

### Weekly Full Tests
- Run complete integration test
- Test all features in UI
- Check database integrity
- Review logs for errors
- Performance benchmarking

---

## Reporting Issues

When reporting bugs, include:
1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Error messages** (from console or logs)
5. **Environment details** (OS, browser, Python version)
6. **Screenshots** (if UI issue)

Example:
```
Title: Hint 3 not displaying for hard problems

Steps:
1. Generate hard difficulty algebra problem
2. Click "Hint 3" button
3. Observe behavior

Expected: Third hint displays in yellow box
Actual: Hint 3 box is empty

Error: Console shows "TypeError: hints[2] is undefined"

Environment: Ubuntu 22.04, Chrome 120, Python 3.11
```

---

## Test Automation Setup (Future)

```bash
# Install pytest
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=html
```
