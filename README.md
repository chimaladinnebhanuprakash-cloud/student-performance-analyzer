# Student Performance Analyzer

A complete full-stack web application for analyzing student performance with authentication, profile management, performance analysis, and an AI assistant chatbot.

## Features

✨ **User Authentication**
- Secure signup and login
- Password hashing with bcrypt
- Session-based authentication

📊 **Performance Analysis**
- Subject-wise marks tracking
- Attendance monitoring
- Study hours analysis
- Backlog tracking
- Intelligent scoring algorithm
- Personalized improvement suggestions

🏠 **Dashboard**
- Performance overview with summary cards
- Interactive performance trend charts
- Quick access to all features

👤 **Student Profile**
- Editable profile information
- Course and semester tracking
- College information

🤖 **AI Study Assistant**
- Rule-based conversational AI
- Personalized study tips
- Time management guidance
- Motivation and support
- Context-aware responses based on performance

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: SQLite
- **Charts**: Chart.js
- **Styling**: Custom CSS with glassmorphism and dark mode

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

## Installation & Setup

### 1. Clone or Download the Project

Navigate to the project directory:
```bash
cd SPA
```

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (cross-origin resource sharing)
- bcrypt (password hashing)

### 3. Database Setup

The database will be automatically created when you first run the application. The SQLite database file (`student_performance.db`) will be created in the project root directory.

## Running the Application

### 1. Start the Backend Server

From the `backend` directory:

```bash
python app.py
```

You should see:
```
==================================================
Student Performance Analyzer
==================================================
Server starting on http://localhost:5000
==================================================
```

### 2. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

The login page will appear.

## Usage Guide

### First Time Setup

1. **Create an Account**
   - Click "Sign up here" on the login page
   - Fill in your full name, email, and password
   - Click "Create Account"
   - You'll be redirected to the login page

2. **Login**
   - Enter your email and password
   - Click "Login"
   - You'll be redirected to the dashboard

3. **Complete Your Profile**
   - Click on the "Profile" tab
   - Fill in your age, gender, course, semester, and college
   - Click "Save Profile"

### Using the Performance Analyzer

1. Navigate to the "Performance Analyzer" tab
2. Enter your subject-wise marks (click "+ Add Subject" for more subjects)
3. Enter your attendance percentage
4. Enter your average study hours per day
5. Enter number of backlogs (if any)
6. Click "Analyze Performance"
7. View your performance score, category, and personalized suggestions

### Using the AI Assistant

1. Navigate to the "AI Assistant" tab
2. Type your question or concern in the chat input
3. Press "Send" or hit Enter
4. The AI will provide personalized guidance based on your profile and performance

**Example questions to ask:**
- "How can I improve my performance?"
- "Give me study tips"
- "How should I manage my time?"
- "I'm feeling stressed about exams"
- "How do I clear my backlogs?"

### Viewing Your Progress

1. Navigate to the "Home" tab
2. View your performance summary cards
3. Check the performance trend chart to see your progress over time

## Project Structure

```
SPA/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database operations
│   ├── auth.py             # Authentication utilities
│   ├── analyzer.py         # Performance analysis logic
│   ├── chatbot.py          # AI assistant logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Login page
│   ├── signup.html         # Registration page
│   ├── dashboard.html      # Main dashboard
│   ├── home.html           # Home page content
│   ├── profile.html        # Profile page content
│   ├── analyzer.html       # Performance analyzer content
│   ├── chat.html           # AI assistant content
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       ├── auth.js         # Authentication logic
│       ├── dashboard.js    # Dashboard navigation
│       ├── home.js         # Home page logic
│       ├── profile.js      # Profile management
│       ├── analyzer.js     # Performance analyzer
│       └── chat.js         # Chatbot interface
├── database/
│   └── schema.sql          # Database schema
├── student_performance.db  # SQLite database (auto-created)
└── README.md               # This file
```

## Performance Scoring Algorithm

The performance score is calculated using a weighted formula:

- **Marks (50%)**: Average of all subject marks
- **Attendance (25%)**: Attendance percentage
- **Study Hours (15%)**: Normalized study hours (8 hours = 100%)
- **Backlogs (10%)**: Penalty for backlogs

**Categories:**
- **Excellent**: Score ≥ 85
- **Good**: Score ≥ 70
- **Average**: Score ≥ 50
- **Needs Improvement**: Score < 50

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, edit `backend/app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or any available port
```

### Database Errors

If you encounter database errors, delete the `student_performance.db` file and restart the server. The database will be recreated automatically.

### CORS Errors

Make sure you're accessing the application through `http://localhost:5000` and not by opening the HTML files directly in the browser.

### Module Not Found Errors

Make sure all dependencies are installed:
```bash
cd backend
pip install -r requirements.txt
```

## Security Notes

- Passwords are hashed using bcrypt before storage
- Session-based authentication protects all dashboard routes
- Input validation on both frontend and backend
- SQL injection protection through parameterized queries

## Future Enhancements

- Export performance reports as PDF
- Email notifications for low performance
- Comparison with class average
- Goal setting and tracking
- Mobile app version
- Integration with external APIs for study resources

## License

This project is created for educational purposes.

## Support

For issues or questions, please check the troubleshooting section above or review the code comments for detailed implementation information.

---

**Enjoy using Student Performance Analyzer!** 🎓📚✨
