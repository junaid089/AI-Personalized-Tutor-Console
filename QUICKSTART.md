# Quick Start Guide - AI Personalized Tutor Console

## 🚀 Quick Setup (5 minutes)

### 1. Clone & Enter Directory
```bash
git clone git@github.com:junaid089/AI-Personalized-Tutor-Console.git
cd AI-Personalized-Tutor-Console
```

### 2. Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE tutor_db;"

# macOS
brew install postgresql
brew services start postgresql
createdb tutor_db
```

### 3. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Already configured in backend/.env
# EMERGENT_LLM_KEY=sk-emergent-347D1Bc865f97F4353
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tutor_db
```

### 5. Run the Application
```bash
cd /path/to/AI-Personalized-Tutor-Console/backend
python server.py
```

### 6. Open Browser
```
http://localhost:8001
```

## 🎯 First Steps

1. **Create a Student**
   - Click "Student Profiles"
   - Click "+ Add New Student"
   - Fill in details and save

2. **Try Practice Problems**
   - Click "Practice Problems"
   - Enter topic: "Algebra"
   - Click "Generate Problems"
   - Try hints and solutions!

3. **View Progress**
   - Click "Progress Tracking"
   - Select your student
   - Click "Load Progress"

## ⚡ Key Features to Try

- **💡 3-Tier Hint System**: Progressive hints from gentle to detailed
- **📝 Step-by-Step Solutions**: Complete explanations with reasoning
- **📊 Progress Dashboard**: Mastery scores and recommendations
- **📚 Lesson Plans**: AI-generated personalized lessons
- **🧪 Diagnostic Tests**: Assess baseline knowledge

## 🔧 Troubleshooting

### Backend won't start?
```bash
tail -f /var/log/supervisor/backend.err.log
```

### Database error?
```bash
sudo service postgresql status
sudo -u postgres psql -c "CREATE DATABASE tutor_db;"
```

### Module not found?
```bash
cd backend
pip install -r requirements.txt
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

## 🆘 Need Help?

- Check [README.md](README.md) Troubleshooting section
- Open an issue on GitHub
- Review API docs at: http://localhost:8001/docs
