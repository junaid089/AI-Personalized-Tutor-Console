# AI-Personalized-Tutor-Console

An AI-powered educational platform that delivers personalized, scaffolded instruction and practice tailored to each learner's profile. This system maximizes mastery through adaptive content generation, tiered hints, step-by-step solutions, and transparent progress tracking.

## 📋 Features

### Core Features (Implemented Priority Order)

1. **🎯 Hint System & Step-by-Step Solutions** (Priority 1)
   - Three-tiered progressive hints for each practice problem
   - Detailed step-by-step solution explanations
   - Interactive problem-solving interface

2. **📊 Progress Tracking & Recommendations** (Priority 2)
   - Mastery score calculation (0-100 scale)
   - Personalized progress summaries
   - Strengths and target areas identification
   - AI-generated next-step recommendations

3. **📚 Lesson Plan Generation** (Priority 3)
   - Comprehensive lesson plans with learning objectives
   - Time-estimated activities
   - Personalized based on student profile
   - Adaptive to learning style and pacing preferences

4. **🧪 Diagnostic Assessment** (Priority 4)
   - Baseline mastery detection
   - Varied difficulty question generation
   - Skill mapping and misconception identification
   - Interactive quiz interface

### Additional Features

- **Student Profile Management**: Create and manage student profiles with learning styles, pacing preferences, and goals
- **Adaptive Practice Problems**: AI-generated problems tailored to student level and topic
- **Privacy-First Design**: Structured data storage with PostgreSQL
- **RESTful API**: Complete JSON-based API for all operations
- **Responsive UI**: Bootstrap-based interface for desktop and mobile

## 🛠 Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- **Database**: PostgreSQL
- **AI Integration**: Claude (Anthropic Sonnet 4) via Emergent LLM Key
- **AI Library**: emergentintegrations (custom integration library)

## 📦 Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Git
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone git@github.com:junaid089/AI-Personalized-Tutor-Console.git
cd AI-Personalized-Tutor-Console
```

### Step 2: Install PostgreSQL

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

#### On macOS:
```bash
brew install postgresql
brew services start postgresql
```

#### On Windows:
Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/)

### Step 3: Create Database

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE tutor_db;

# Set password for postgres user (if needed)
ALTER USER postgres WITH PASSWORD 'postgres';

# Exit
\q
```

### Step 4: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
cat > .env << EOF
EMERGENT_LLM_KEY=sk-emergent-347D1Bc865f97F4353
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tutor_db
EOF
```

**Note**: The Emergent LLM key provided above is a demo key. Replace it with your own key if you have one, or use the provided universal key for testing.

### Step 6: Run the Application

#### Option A: Using uvicorn directly

```bash
# From the backend directory
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

#### Option B: Using supervisor (recommended for production)

```bash
# Configure supervisor
sudo cp /path/to/backend.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start backend
```

### Step 7: Access the Application

Open your browser and navigate to:
```
http://localhost:8001
```

The API documentation is available at:
```
http://localhost:8001/docs
```

## 🚀 Usage Guide

### 1. Creating a Student Profile

1. Navigate to the **Student Profiles** section
2. Click "**+ Add New Student**"
3. Fill in the student details:
   - Name (required)
   - Age Group
   - Grade Level
   - Learning Style (visual, auditory, kinesthetic, reading/writing, or mixed)
   - Pacing Preference (slow, medium, fast)
   - Goals
4. Click "**Save Student**"

### 2. Generating Practice Problems with Hints

1. Navigate to **Practice Problems** section
2. Enter a topic (e.g., "Algebra", "Fractions", "World War II")
3. Select difficulty level (easy, medium, hard)
4. Choose number of problems (1-10)
5. Click "**Generate Problems**"
6. For each problem:
   - Click "**💡 Hint 1**" for a gentle nudge
   - Click "**💡 Hint 2**" for more specific guidance
   - Click "**💡 Hint 3**" for step-by-step outline
   - Click "**✓ Show Solution**" for complete solution

### 3. Tracking Progress

1. Navigate to **Progress Tracking** section
2. Select a student from the dropdown
3. Click "**Load Progress**"
4. View:
   - Mastery scores for each topic
   - Strengths and areas to improve
   - Personalized recommendations

### 4. Creating Lesson Plans

1. Navigate to **Lesson Plans** section
2. Select a student
3. Enter topic (e.g., "Introduction to Calculus")
4. Enter unit outline (comma-separated: "Limits, Derivatives, Applications")
5. Set session length in minutes
6. Click "**Generate Lesson Plan**"
7. View objectives, activities, and materials

### 5. Running Diagnostic Assessments

1. Navigate to **Diagnostic** section
2. Enter topic
3. Set number of questions (3-10)
4. Click "**Generate Assessment**"
5. Take the quiz by clicking answer options
6. View immediate feedback

## 📚 API Documentation

### Base URL
```
http://localhost:8001/api
```

### Key Endpoints

#### Student Management

- **POST** `/api/students` - Create new student
- **GET** `/api/students` - Get all students
- **GET** `/api/students/{student_id}` - Get specific student

#### Hint System

- **POST** `/api/hints` - Generate 3 tiered hints
  ```json
  {
    "problem": "Solve 2x + 5 = 15",
    "difficulty": "medium",
    "topic": "Algebra"
  }
  ```

- **POST** `/api/solutions` - Generate step-by-step solution
  ```json
  {
    "problem": "Solve 2x + 5 = 15",
    "topic": "Algebra"
  }
  ```

#### Practice Problems

- **POST** `/api/problems` - Generate practice problems
  ```json
  {
    "topic": "Fractions",
    "difficulty": "medium",
    "count": 3
  }
  ```

#### Progress Tracking

- **POST** `/api/progress` - Calculate progress and mastery
  ```json
  {
    "student_id": "uuid",
    "topic": "Algebra",
    "attempts": [{"correct": true}, {"correct": false}],
    "hints_used": [["hint1"], ["hint1", "hint2"]]
  }
  ```

- **GET** `/api/progress/{student_id}` - Get student progress

#### Lesson Plans

- **POST** `/api/lesson-plans` - Generate lesson plan
  ```json
  {
    "student_id": "uuid",
    "topic": "Calculus",
    "unit_outline": ["Limits", "Derivatives"],
    "session_length": 45
  }
  ```

#### Diagnostic Assessment

- **POST** `/api/diagnostic` - Generate diagnostic quiz
  ```json
  {
    "topic": "Fractions",
    "num_questions": 5
  }
  ```

Full interactive API documentation available at: `http://localhost:8001/docs`

## 🧪 Testing

### Backend API Testing with curl

```bash
# Health check
curl http://localhost:8001/api/health

# Create a student
curl -X POST http://localhost:8001/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "grade_level": "7th Grade",
    "learning_style": "visual",
    "pacing_pref": "medium"
  }'

# Generate hints
curl -X POST http://localhost:8001/api/hints \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "What is 15% of 80?",
    "difficulty": "medium",
    "topic": "Percentages"
  }'
```

### Frontend Testing

1. Open browser console (F12)
2. Check for JavaScript errors
3. Test each section of the UI
4. Verify API calls in Network tab

## 📁 Project Structure

```
AI-Personalized-Tutor-Console/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── database.py            # Database configuration
│   ├── models.py              # SQLAlchemy models
│   ├── ai_service.py          # AI integration service
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── templates/
│   │   └── index.html        # Main HTML page
│   └── static/
│       ├── css/
│       │   └── style.css     # Custom styles
│       └── js/
│           └── app.js        # Frontend JavaScript
├── prompts/
│   └── tutor_prompts.txt     # AI prompt templates
└── README.md                  # This file
```

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMERGENT_LLM_KEY` | Universal LLM API key | Required |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/tutor_db` |

## 🐛 Troubleshooting

### Issue: Database connection error

**Solution**: Ensure PostgreSQL is running and the database exists
```bash
sudo service postgresql status
sudo -u postgres psql -c "CREATE DATABASE tutor_db;"
```

### Issue: Backend not starting

**Solution**: Check logs for errors
```bash
tail -f /var/log/supervisor/backend.err.log
```

### Issue: AI API key error

**Solution**: Verify the `EMERGENT_LLM_KEY` in `.env` file
```bash
cat backend/.env
```

### Issue: Module not found errors

**Solution**: Reinstall dependencies
```bash
cd backend
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **Junaid** - [GitHub Profile](https://github.com/junaid089)

## 🙏 Acknowledgments

- **Emergent AI** for providing the universal LLM integration
- **Anthropic** for Claude AI model
- **FastAPI** for the excellent web framework
- **Bootstrap** for the responsive UI framework

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: [Your contact information]

## 🗺 Roadmap

### Completed ✅
- ✅ Student profile management
- ✅ Hint system with 3 tiers
- ✅ Step-by-step solutions
- ✅ Progress tracking with mastery scores
- ✅ Lesson plan generation
- ✅ Diagnostic assessments
- ✅ RESTful API
- ✅ Bootstrap UI

### Future Enhancements 🚀
- 🔄 Real-time collaborative learning
- 🔄 Multiple language support
- 🔄 Video lesson integration
- 🔄 Gamification with achievements
- 🔄 Parent/teacher dashboard
- 🔄 Mobile app (React Native)
- 🔄 Integration with Learning Management Systems (LMS)
- 🔄 Accessibility improvements (WCAG 2.1 AA compliance)

---

**Made with ❤️ for personalized education**
