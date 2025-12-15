# StudyTrackr 📚📊

StudyTrackr is a cloud-based web application designed to help students organize their academic life by tracking courses, study sessions, and estimating GPA. The application allows users to securely register, log in, manage their data, and visualize study habits through charts.

This project was developed as a **final project** for a university-level software development course, focusing on full-stack development and cloud-ready web applications.

---

## 🚀 Features

- **User Authentication**
  - Secure user registration and login
  - Password hashing using Werkzeug
- **Course Management**
  - Add and delete courses
  - Store estimated grades for GPA calculation
- **Study Session Tracking**
  - Log study sessions with date, duration, and notes
  - View and delete past sessions
- **GPA Calculation**
  - Automatic GPA estimation based on course grades
- **Data Visualization**
  - Bar chart showing total study hours per course using Chart.js
- **Responsive UI**
  - Built with Bootstrap for mobile and desktop support

---

## 🛠️ Technology Stack

### Front-End
- HTML5
- CSS3
- Bootstrap 5
- Chart.js

### Back-End
- Python 3
- Flask
- Flask-SQLAlchemy

### Database
- SQLite (local development)

---

## 📂 Project Structure

Studytrckr/
├── app.py
├── requirements.txt
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── courses.html
│ └── sessions.html
├── static/
│ └── (CSS / JS files)
└── instance/
└── studytrackr.db

yaml
Copy code

---

## ⚙️ Installation & Setup

Follow the steps below to run the application locally:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/Studytrckr.git
cd Studytrckr
2️⃣ Create and activate a virtual environment
bash
Copy code
python -m venv .venv
.venv\Scripts\activate   # Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the application
bash
Copy code
python app.py
The app will be available at:

cpp
Copy code
http://127.0.0.1:5000
