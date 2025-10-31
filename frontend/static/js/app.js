// Global state
let currentStudent = null;
let currentProblems = [];
let problemAttempts = [];
let hintsUsed = [];

// API Base URL
const API_BASE = '/api';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadStudents();
    setupNavigation();
});

// Navigation
function setupNavigation() {
    const navButtons = document.querySelectorAll('[data-section]');
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const section = this.getAttribute('data-section');
            showSection(section);
            
            // Update active state
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.style.display = 'none');
    
    // Show selected section
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // Load data for specific sections
    if (sectionName === 'students') {
        loadStudents();
    } else if (sectionName === 'progress') {
        loadStudentSelects();
    } else if (sectionName === 'lessons') {
        loadStudentSelects();
    }
}

// Student Management
async function loadStudents() {
    try {
        const response = await fetch(`${API_BASE}/students`);
        const students = await response.json();
        displayStudents(students);
        updateStudentSelects(students);
    } catch (error) {
        console.error('Error loading students:', error);
        showAlert('Error loading students', 'danger');
    }
}

function displayStudents(students) {
    const container = document.getElementById('students-list');
    
    if (students.length === 0) {
        container.innerHTML = '<div class=\"col-12\"><p class=\"text-muted\">No students yet. Add your first student!</p></div>';
        return;
    }
    
    container.innerHTML = students.map(student => `
        <div class=\"col-md-6 mb-3\">
            <div class=\"card student-card\">
                <div class=\"card-body\">
                    <h5 class=\"card-title\">${student.name}</h5>
                    <p class=\"card-text\">
                        <strong>Grade:</strong> ${student.grade_level || 'N/A'}<br>
                        <strong>Learning Style:</strong> ${student.learning_style}<br>
                        <strong>Pacing:</strong> ${student.pacing_pref}
                    </p>
                    <span class=\"badge bg-primary badge-lg\">Mastery: ${student.prior_mastery}%</span>
                </div>
            </div>
        </div>
    `).join('');
}

function updateStudentSelects(students) {
    const progressSelect = document.getElementById('progress-student-select');
    const lessonSelect = document.getElementById('lesson-student-select');
    
    const options = students.map(s => 
        `<option value=\"${s.id}\">${s.name}</option>`
    ).join('');
    
    if (progressSelect) progressSelect.innerHTML = '<option value=\"\">Select a student</option>' + options;
    if (lessonSelect) lessonSelect.innerHTML = '<option value=\"\">Select a student</option>' + options;
}

function loadStudentSelects() {
    loadStudents();
}

async function saveStudent() {
    const studentData = {
        name: document.getElementById('student-name').value,
        age_group: document.getElementById('student-age').value,
        grade_level: document.getElementById('student-grade').value,
        learning_style: document.getElementById('student-learning-style').value,
        pacing_pref: document.getElementById('student-pacing').value,
        goals: document.getElementById('student-goals').value
    };
    
    if (!studentData.name) {
        showAlert('Please enter student name', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/students`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(studentData)
        });
        
        if (response.ok) {
            showAlert('Student added successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addStudentModal')).hide();
            document.getElementById('student-form').reset();
            loadStudents();
        }
    } catch (error) {
        console.error('Error saving student:', error);
        showAlert('Error saving student', 'danger');
    }
}

// Practice Problems with Hints
async function generateProblems() {
    const topic = document.getElementById('practice-topic').value;
    const difficulty = document.getElementById('practice-difficulty').value;
    const count = parseInt(document.getElementById('practice-count').value);
    
    if (!topic) {
        showAlert('Please enter a topic', 'warning');
        return;
    }
    
    const container = document.getElementById('problems-list');
    container.innerHTML = '<div class=\"loading\"><div class=\"spinner-border text-primary\" role=\"status\"></div><p class=\"mt-2\">Generating problems...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE}/problems`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, difficulty, count })
        });
        
        const data = await response.json();
        currentProblems = data.problems;
        displayProblems(data.problems, topic, difficulty);
    } catch (error) {
        console.error('Error generating problems:', error);
        container.innerHTML = '<div class=\"alert alert-danger\">Error generating problems</div>';
    }
}

function displayProblems(problems, topic, difficulty) {
    const container = document.getElementById('problems-list');
    
    if (problems.length === 0) {
        container.innerHTML = '<div class=\"alert alert-info\">No problems generated. Please try again.</div>';
        return;
    }
    
    container.innerHTML = problems.map((problem, index) => `
        <div class=\"problem-card\" id=\"problem-${index}\">
            <h5>Problem ${index + 1}</h5>
            <p class=\"lead\">${problem.prompt}</p>
            <div class=\"mb-2\">
                <span class=\"badge bg-info\">Difficulty: ${problem.difficulty || difficulty}</span>
            </div>
            
            <div class=\"btn-group mb-3\" role=\"group\">
                <button class=\"btn btn-hint\" onclick=\"revealHint(${index}, 0, '${topic}', '${problem.prompt}', '${difficulty}')\">
                    💡 Hint 1
                </button>
                <button class=\"btn btn-hint\" onclick=\"revealHint(${index}, 1, '${topic}', '${problem.prompt}', '${difficulty}')\">
                    💡 Hint 2
                </button>
                <button class=\"btn btn-hint\" onclick=\"revealHint(${index}, 2, '${topic}', '${problem.prompt}', '${difficulty}')\">
                    💡 Hint 3
                </button>
                <button class=\"btn btn-info\" onclick=\"showSolution(${index}, '${topic}', '${problem.prompt}')\">
                    ✓ Show Solution
                </button>
            </div>
            
            <div id=\"hints-${index}\" class=\"hints-container\"></div>
            <div id=\"solution-${index}\" class=\"solution-container\"></div>
        </div>
    `).join('');
}

async function revealHint(problemIndex, hintLevel, topic, problem, difficulty) {
    const hintsContainer = document.getElementById(`hints-${problemIndex}`);
    
    // Check if hints already exist
    if (!hintsUsed[problemIndex]) {
        hintsUsed[problemIndex] = [];
        
        // Generate all hints at once
        const response = await fetch(`${API_BASE}/hints`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                problem: problem,
                difficulty: difficulty,
                topic: topic
            })
        });
        
        const data = await response.json();
        hintsUsed[problemIndex] = data.hints;
    }
    
    // Display the requested hint
    const hint = hintsUsed[problemIndex][hintLevel];
    if (hint) {
        const hintElement = document.createElement('div');
        hintElement.className = 'hint-box';
        hintElement.innerHTML = `<strong>Hint ${hintLevel + 1}:</strong> ${hint}`;
        hintsContainer.appendChild(hintElement);
    }
}

async function showSolution(problemIndex, topic, problem) {
    const solutionContainer = document.getElementById(`solution-${problemIndex}`);
    solutionContainer.innerHTML = '<div class=\"loading\"><div class=\"spinner-border spinner-border-sm text-info\"></div> Generating solution...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/solutions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ problem: problem, topic: topic })
        });
        
        const solution = await response.json();
        
        solutionContainer.innerHTML = `
            <div class=\"solution-box\">
                <h6>Step-by-Step Solution:</h6>
                ${solution.steps.map((step, i) => `
                    <div class=\"step\">${i + 1}. ${step}</div>
                `).join('')}
                <div class=\"mt-3\">
                    <strong>Answer:</strong> ${solution.answer}
                </div>
                <div class=\"mt-2\">
                    <em>${solution.explanation}</em>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error generating solution:', error);
        solutionContainer.innerHTML = '<div class=\"alert alert-danger\">Error generating solution</div>';
    }
}

// Progress Tracking
async function loadProgress() {
    const studentId = document.getElementById('progress-student-select').value;
    
    if (!studentId) {
        showAlert('Please select a student', 'warning');
        return;
    }
    
    const container = document.getElementById('progress-display');
    container.innerHTML = '<div class=\"loading\"><div class=\"spinner-border text-primary\"></div></div>';
    
    try {
        const response = await fetch(`${API_BASE}/progress/${studentId}`);
        const progressData = await response.json();
        
        displayProgress(progressData);
    } catch (error) {
        console.error('Error loading progress:', error);
        container.innerHTML = '<div class=\"alert alert-danger\">Error loading progress</div>';
    }
}

function displayProgress(progressData) {
    const container = document.getElementById('progress-display');
    
    if (progressData.length === 0) {
        container.innerHTML = '<div class=\"alert alert-info\">No progress data available yet.</div>';
        return;
    }
    
    container.innerHTML = progressData.map(progress => `
        <div class=\"progress-summary\">
            <div class=\"row\">
                <div class=\"col-md-3 text-center\">
                    <div class=\"mastery-score\">${progress.mastery_score}</div>
                    <div>Mastery Score</div>
                </div>
                <div class=\"col-md-9\">
                    <h5>${progress.topic}</h5>
                    <div class=\"mt-3\">
                        <strong>✓ Strengths:</strong>
                        <ul>
                            ${progress.strengths.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                    </div>
                    <div class=\"mt-2\">
                        <strong>⚠ Areas to Improve:</strong>
                        <ul>
                            ${progress.target_areas.map(a => `<li>${a}</li>`).join('')}
                        </ul>
                    </div>
                    <div class=\"mt-2\">
                        <strong>→ Recommendations:</strong>
                        <ul>
                            ${progress.recommendations.map(r => `<li>${r}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Lesson Plans
async function generateLessonPlan() {
    const studentId = document.getElementById('lesson-student-select').value;
    const topic = document.getElementById('lesson-topic').value;
    const outline = document.getElementById('lesson-outline').value;
    const duration = parseInt(document.getElementById('lesson-duration').value);
    
    if (!studentId || !topic || !outline) {
        showAlert('Please fill in all fields', 'warning');
        return;
    }
    
    const unitOutline = outline.split(',').map(s => s.trim());
    
    const container = document.getElementById('lesson-display');
    container.innerHTML = '<div class=\"loading\"><div class=\"spinner-border text-success\"></div><p class=\"mt-2\">Generating lesson plan...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE}/lesson-plans`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: studentId,
                topic: topic,
                unit_outline: unitOutline,
                session_length: duration
            })
        });
        
        const lessonPlan = await response.json();
        displayLessonPlan(lessonPlan, topic);
    } catch (error) {
        console.error('Error generating lesson plan:', error);
        container.innerHTML = '<div class=\"alert alert-danger\">Error generating lesson plan</div>';
    }
}

function displayLessonPlan(plan, topic) {
    const container = document.getElementById('lesson-display');
    
    container.innerHTML = `
        <div class=\"card\">
            <div class=\"card-header bg-success text-white\">
                <h5>Lesson Plan: ${topic}</h5>
            </div>
            <div class=\"card-body\">
                <h6>Learning Objectives:</h6>
                ${plan.objectives.map(obj => `
                    <div class=\"lesson-objective\">${obj}</div>
                `).join('')}
                
                <h6 class=\"mt-4\">Activities:</h6>
                ${plan.activities.map((activity, i) => `
                    <div class=\"activity-item\">
                        <div class=\"d-flex justify-content-between align-items-start\">
                            <div>
                                <strong>Activity ${i + 1}: ${activity.title}</strong>
                                <p class=\"mb-0 mt-2\">${activity.description}</p>
                            </div>
                            <span class=\"badge bg-info\">${activity.time_minutes} min</span>
                        </div>
                    </div>
                `).join('')}
                
                <h6 class=\"mt-4\">Materials Needed:</h6>
                <ul>
                    ${plan.materials.map(material => `<li>${material}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
}

// Diagnostic Assessment
async function generateDiagnostic() {
    const topic = document.getElementById('diagnostic-topic').value;
    const numQuestions = parseInt(document.getElementById('diagnostic-questions').value);
    
    if (!topic) {
        showAlert('Please enter a topic', 'warning');
        return;
    }
    
    const container = document.getElementById('diagnostic-display');
    container.innerHTML = '<div class=\"loading\"><div class=\"spinner-border text-primary\"></div><p class=\"mt-2\">Generating diagnostic assessment...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE}/diagnostic`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, num_questions: numQuestions })
        });
        
        const assessment = await response.json();
        displayDiagnostic(assessment, topic);
    } catch (error) {
        console.error('Error generating diagnostic:', error);
        container.innerHTML = '<div class=\"alert alert-danger\">Error generating diagnostic</div>';
    }
}

function displayDiagnostic(assessment, topic) {
    const container = document.getElementById('diagnostic-display');
    
    if (!assessment.questions || assessment.questions.length === 0) {
        container.innerHTML = '<div class=\"alert alert-info\">No questions generated. Please try again.</div>';
        return;
    }
    
    container.innerHTML = `
        <div class=\"card\">
            <div class=\"card-header bg-primary text-white\">
                <h5>Diagnostic Assessment: ${topic}</h5>
            </div>
            <div class=\"card-body\">
                ${assessment.questions.map((q, index) => `
                    <div class=\"diagnostic-question\">
                        <h6>Question ${index + 1}:</h6>
                        <p>${q.question}</p>
                        <div class=\"mt-2\">
                            ${q.options.map((option, optIndex) => `
                                <button class=\"btn btn-outline-primary option-button\" onclick=\"checkAnswer(${index}, '${option}', '${q.correct_answer}')\">\n                                    ${option}\n                                </button>\n                            `).join('')}
                        </div>
                        <div id=\"feedback-${index}\" class=\"mt-2\"></div>
                        <small class=\"text-muted\">Tests: ${q.skill_tested} | Difficulty: ${q.difficulty}</small>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function checkAnswer(questionIndex, selected, correct) {
    const feedback = document.getElementById(`feedback-${questionIndex}`);
    
    if (selected === correct) {
        feedback.innerHTML = '<div class=\"alert alert-success\">✓ Correct!</div>';
    } else {
        feedback.innerHTML = `<div class=\"alert alert-danger\">✗ Incorrect. The correct answer is: ${correct}</div>`;
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"alert\"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}
