from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
DATABASE = "career.db"


# ================= DATABASE =================

def create_database():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            interest TEXT NOT NULL,
            skill TEXT NOT NULL,
            career TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ================= CAREER DATA =================

CAREERS = {
    "Web Development": {
        "career": "Web Developer",
        "skills": ["HTML", "CSS", "JavaScript", "Git", "React"],
        "projects": [
            "Personal Portfolio Website",
            "Student Management System",
            "Online Shopping Website"
        ],
        "roadmap": [
            "1. Learn HTML basics",
            "2. Learn CSS and responsive design",
            "3. Learn JavaScript",
            "4. Learn Git and GitHub",
            "5. Learn React or another frontend framework",
            "6. Build 2-3 real projects"
        ],
        "guidance": [
            "Practice HTML and CSS by building small web pages.",
            "Use JavaScript to add buttons, forms and interactive features.",
            "Build projects instead of only watching tutorials.",
            "Upload completed projects to GitHub.",
            "Create a portfolio website to show your work."
        ],
        "week": [
            "Monday: HTML/CSS practice",
            "Tuesday: JavaScript basics",
            "Wednesday: Build one small webpage",
            "Thursday: JavaScript practice",
            "Friday: Improve your project",
            "Saturday: Learn Git/GitHub",
            "Sunday: Revision and project testing"
        ]
    },

    "Data Analysis": {
        "career": "Data Analyst",
        "skills": ["Python", "NumPy", "Pandas", "SQL", "Excel", "Data Visualization"],
        "projects": [
            "Sales Data Analysis",
            "Google Play Store Analysis",
            "Student Marks Analysis"
        ],
        "roadmap": [
            "1. Learn Python basics",
            "2. Learn NumPy",
            "3. Learn Pandas",
            "4. Learn SQL",
            "5. Learn Excel",
            "6. Learn charts and data visualization",
            "7. Build data analysis projects"
        ],
        "guidance": [
            "Practice Python with small data problems.",
            "Learn Pandas for reading and cleaning CSV files.",
            "Practice SQL queries using sample databases.",
            "Create charts from real datasets.",
            "Explain your findings in simple language.",
            "Build a small portfolio of analysis projects."
        ],
        "week": [
            "Monday: Python practice",
            "Tuesday: NumPy and Pandas",
            "Wednesday: CSV data cleaning",
            "Thursday: SQL practice",
            "Friday: Create charts",
            "Saturday: Work on one dataset",
            "Sunday: Review your analysis"
        ]
    },

    "Software Development": {
        "career": "Software Developer",
        "skills": ["Java", "Python", "SQL", "OOP", "Git", "Problem Solving"],
        "projects": [
            "Library Management System",
            "Student Management System",
            "Expense Management System"
        ],
        "roadmap": [
            "1. Learn programming fundamentals",
            "2. Learn OOP concepts",
            "3. Practice data structures",
            "4. Learn SQL and databases",
            "5. Learn Git and GitHub",
            "6. Build complete applications"
        ],
        "guidance": [
            "Practice programming every day.",
            "Understand logic instead of only copying code.",
            "Solve small programming problems.",
            "Learn object-oriented programming.",
            "Connect applications to a database.",
            "Build projects that solve real student problems."
        ],
        "week": [
            "Monday: Programming fundamentals",
            "Tuesday: OOP practice",
            "Wednesday: Problem solving",
            "Thursday: SQL/database practice",
            "Friday: Project development",
            "Saturday: Debug and improve project",
            "Sunday: Revision"
        ]
    },

    "Cyber Security": {
        "career": "Cyber Security Analyst",
        "skills": ["Networking", "Linux", "Python", "Cyber Security Basics", "Security Tools"],
        "projects": [
            "Password Strength Checker",
            "Network Information Dashboard",
            "Cyber Security Awareness Website"
        ],
        "roadmap": [
            "1. Learn computer networks",
            "2. Learn Linux basics",
            "3. Learn Python basics",
            "4. Learn security concepts",
            "5. Study authentication and access control",
            "6. Practice only in authorized lab environments"
        ],
        "guidance": [
            "Learn networking fundamentals first.",
            "Practice Linux commands in a safe local environment.",
            "Learn how authentication and permissions work.",
            "Use legal practice labs designed for students.",
            "Document what you learn in notes and projects."
        ],
        "week": [
            "Monday: Networking",
            "Tuesday: Linux basics",
            "Wednesday: Python practice",
            "Thursday: Security concepts",
            "Friday: Safe lab practice",
            "Saturday: Security project",
            "Sunday: Revision"
        ]
    },

    "Database": {
        "career": "Database Administrator",
        "skills": ["SQL", "MySQL", "Database Design", "Normalization", "Backup Basics"],
        "projects": [
            "College Database System",
            "Library Database",
            "Hospital Management Database"
        ],
        "roadmap": [
            "1. Learn SQL basics",
            "2. Learn tables and relationships",
            "3. Learn joins and subqueries",
            "4. Learn normalization",
            "5. Learn database design",
            "6. Build database projects"
        ],
        "guidance": [
            "Practice SELECT, INSERT, UPDATE and DELETE queries.",
            "Learn primary keys and foreign keys.",
            "Practice joins using small databases.",
            "Draw an ER diagram before building a project.",
            "Use meaningful table and column names.",
            "Learn basic database security and backup concepts."
        ],
        "week": [
            "Monday: SQL basics",
            "Tuesday: SELECT and filtering",
            "Wednesday: Joins",
            "Thursday: Database design",
            "Friday: Build tables",
            "Saturday: Project practice",
            "Sunday: Revision"
        ]
    }
}


# ================= RECOMMENDATION =================

def recommend(interest, skill):
    data = CAREERS.get(interest, CAREERS["Software Development"])

    current = skill.lower()

    # Simple skill-gap logic
    missing = []
    for item in data["skills"]:
        if item.lower() not in current:
            missing.append(item)

    if not missing:
        missing = ["Practice advanced projects and improve problem solving"]

    return data, missing


# ================= WEBSITE =================

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Career Guidance System</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    color: #1f2937;
}

header {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    text-align: center;
    padding: 35px 15px;
}

header h1 {
    margin: 0;
    font-size: 32px;
}

header p {
    margin-top: 10px;
}

.container {
    width: 92%;
    max-width: 1050px;
    margin: 30px auto;
}

.card {
    background: white;
    padding: 28px;
    margin-bottom: 25px;
    border-radius: 15px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.08);
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
}

label {
    display: block;
    margin-bottom: 7px;
    font-weight: bold;
}

input, select {
    width: 100%;
    padding: 12px;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    font-size: 15px;
}

button {
    width: 100%;
    padding: 14px;
    margin-top: 22px;
    border: none;
    border-radius: 8px;
    background: #4f46e5;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background: #3730a3;
}

.result-title {
    color: #4f46e5;
}

.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.info {
    background: #f8fafc;
    padding: 18px;
    border-radius: 10px;
    border-left: 4px solid #4f46e5;
}

.info h3 {
    margin-top: 0;
    color: #4f46e5;
}

li {
    margin: 9px 0;
    line-height: 1.4;
}

.progress-box {
    background: #eef2ff;
    padding: 18px;
    border-radius: 10px;
}

footer {
    background: #111827;
    color: white;
    text-align: center;
    padding: 22px;
    margin-top: 40px;
}

@media (max-width: 700px) {
    .form-grid, .grid {
        grid-template-columns: 1fr;
    }

    header h1 {
        font-size: 25px;
    }
}

</style>

</head>

<body>

<header>

<h1>🎓 AI Career Guidance System</h1>

<p>Career • Skills • Roadmap • Projects • Study Plan</p>

</header>


<div class="container">

<div class="card">

<h2>👩‍🎓 Student Profile</h2>

<form method="POST">

<div class="form-grid">

<div>

<label>Student Name</label>

<input
type="text"
name="name"
placeholder="Enter your name"
required
>

</div>


<div>

<label>Area of Interest</label>

<select name="interest" required>

<option value="">Select Interest</option>

{% for item in interests %}

<option value="{{ item }}">{{ item }}</option>

{% endfor %}

</select>

</div>


<div>

<label>Current Skill</label>

<select name="skill" required>

<option value="">Select Current Skill</option>

<option value="HTML CSS">HTML / CSS</option>

<option value="Python">Python</option>

<option value="Java">Java</option>

<option value="SQL">SQL</option>

<option value="Networking">Networking</option>

</select>

</div>

</div>

<button type="submit">
Generate My Career Plan
</button>

</form>

</div>


{% if result %}

<div class="card">

<h2 class="result-title">🎯 Your Career Plan</h2>

<p>
<strong>Student:</strong> {{ name }}
</p>

<p>
<strong>Recommended Career:</strong> {{ career }}
</p>

</div>


<div class="grid">

<div class="card info">

<h3>📚 Skills to Learn</h3>

<ul>

{% for item in skills %}

<li>{{ item }}</li>

{% endfor %}

</ul>

</div>


<div class="card info">

<h3>🔎 Your Skill Gap</h3>

<p>
These are the skills you can focus on next:
</p>

<ul>

{% for item in missing %}

<li>{{ item }}</li>

{% endfor %}

</ul>

</div>


<div class="card info">

<h3>🛣️ Learning Roadmap</h3>

<ul>

{% for item in roadmap %}

<li>{{ item }}</li>

{% endfor %}

</ul>

</div>


<div class="card info">

<h3>💡 How to Improve</h3>

<ul>

{% for item in guidance %}

<li>{{ item }}</li>

{% endfor %}

</ul>

</div>


<div class="card info">

<h3>🛠️ Project Ideas</h3>

<ul>

{% for item in projects %}

<li>{{ item }}</li>

{% endfor %}

</ul>

</div>


<div class="card info">

<h3>📅 7-Day Study Plan</h3>

<ul>

{% for item in week %}

<li>{{ item }}</li>

{% endfor %}

</ul>

</div>

</div>


<div class="card progress-box">

<h3>⭐ Student Tip</h3>

<p>
Don't try to learn every technology at once.
Choose one skill, practice it regularly, build projects,
and then move to the next skill.
</p>

<p>
<strong>Suggested routine:</strong>
1 hour learning + 1 hour practical practice each day.
</p>

</div>

{% endif %}

</div>


<footer>

AI-Based Career Guidance and Skill Recommendation System<br>
B.Sc. Computer Science | College Project

</footer>

</body>
</html>
"""


# ================= ROUTE =================

@app.route("/", methods=["GET", "POST"])
def home():

    result = False

    name = ""
    career = ""
    skills = []
    missing = []
    roadmap = []
    guidance = []
    projects = []
    week = []

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        interest = request.form.get("interest", "").strip()
        skill = request.form.get("skill", "").strip()

        if name and interest and skill:

            data, missing = recommend(interest, skill)

            career = data["career"]
            skills = data["skills"]
            roadmap = data["roadmap"]
            guidance = data["guidance"]
            projects = data["projects"]
            week = data["week"]

            conn = sqlite3.connect(DATABASE)

            conn.execute(
                """
                INSERT INTO students
                (name, interest, skill, career)
                VALUES (?, ?, ?, ?)
                """,
                (name, interest, skill, career)
            )

            conn.commit()
            conn.close()

            result = True

    return render_template_string(
        HTML,
        result=result,
        name=name,
        career=career,
        skills=skills,
        missing=missing,
        roadmap=roadmap,
        guidance=guidance,
        projects=projects,
        week=week,
        interests=list(CAREERS.keys())
    )


# ================= START =================

if __name__ == "__main__":

    create_database()

    print()
    print("==========================================")
    print(" AI CAREER GUIDANCE SYSTEM")
    print("==========================================")
    print("Website: http://127.0.0.1:5000")
    print("Keep this terminal open.")
    print("==========================================")
    print()

    app.run(host="127.0.0.1", port=5000, debug=True)
