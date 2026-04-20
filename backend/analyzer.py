"""
Performance analysis logic for Student Performance Analyzer
"""

def calculate_performance_score(subject_marks, attendance, study_hours, backlogs):
    """
    Calculate performance score based on multiple factors
    
    Args:
        subject_marks: dict of subject names and marks (0-100)
        attendance: attendance percentage (0-100)
        study_hours: average study hours per day
        backlogs: number of backlogs
    
    Returns:
        float: performance score (0-100)
    """
    # Calculate average marks
    if subject_marks:
        avg_marks = sum(subject_marks.values()) / len(subject_marks)
    else:
        avg_marks = 0
    
    # Weighted scoring
    marks_weight = 0.50  # 50% weight
    attendance_weight = 0.25  # 25% weight
    study_weight = 0.15  # 15% weight
    backlog_weight = 0.10  # 10% weight
    
    # Calculate components
    marks_score = avg_marks * marks_weight
    attendance_score = attendance * attendance_weight
    
    # Study hours score (normalize to 0-100, assuming 8 hours is excellent)
    study_score = min(study_hours / 8 * 100, 100) * study_weight
    
    # Backlog penalty (each backlog reduces score)
    backlog_penalty = min(backlogs * 10, 100)
    backlog_score = (100 - backlog_penalty) * backlog_weight
    
    # Total score
    total_score = marks_score + attendance_score + study_score + backlog_score
    
    return round(total_score, 2)

def categorize_performance(score):
    """
    Categorize performance based on score
    
    Args:
        score: performance score (0-100)
    
    Returns:
        str: category name
    """
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Needs Improvement"

def generate_explanation(score, category, subject_marks, attendance, study_hours, backlogs):
    """Generate explanation for the performance score"""
    avg_marks = sum(subject_marks.values()) / len(subject_marks) if subject_marks else 0
    
    explanation = f"Your performance score of {score}/100 falls in the '{category}' category. "
    
    if category == "Excellent":
        explanation += "You're doing exceptionally well! Keep up the great work."
    elif category == "Good":
        explanation += "You're performing well, but there's room for improvement."
    elif category == "Average":
        explanation += "Your performance is satisfactory, but you should focus on improving."
    else:
        explanation += "Your performance needs significant improvement. Don't worry, we can help!"
    
    return explanation

def generate_suggestions(score, category, subject_marks, attendance, study_hours, backlogs):
    """
    Generate personalized improvement suggestions
    
    Returns:
        list: list of suggestion strings
    """
    suggestions = []
    avg_marks = sum(subject_marks.values()) / len(subject_marks) if subject_marks else 0
    
    # Marks-based suggestions
    if avg_marks < 60:
        suggestions.append("Focus on understanding core concepts rather than memorization")
        suggestions.append("Create a study schedule and stick to it consistently")
        suggestions.append("Seek help from teachers or peers for difficult topics")
    elif avg_marks < 80:
        suggestions.append("Practice more problems to strengthen your understanding")
        suggestions.append("Review your mistakes and learn from them")
    
    # Find weak subjects
    if subject_marks:
        weak_subjects = [subj for subj, marks in subject_marks.items() if marks < 50]
        if weak_subjects:
            suggestions.append(f"Pay special attention to: {', '.join(weak_subjects)}")
    
    # Attendance-based suggestions
    if attendance < 75:
        suggestions.append("⚠️ Improve your attendance - aim for at least 75%")
        suggestions.append("Regular attendance helps you stay updated with coursework")
    elif attendance < 90:
        suggestions.append("Try to maintain attendance above 90% for better learning")
    
    # Study hours suggestions
    if study_hours < 3:
        suggestions.append("Increase your daily study hours to at least 3-4 hours")
        suggestions.append("Create a distraction-free study environment")
    elif study_hours < 5:
        suggestions.append("Consider increasing study hours during exam periods")
    
    # Backlog suggestions
    if backlogs > 0:
        suggestions.append(f"⚠️ Clear your {backlogs} backlog(s) as soon as possible")
        suggestions.append("Prioritize backlog subjects to avoid accumulation")
    
    # General suggestions based on category
    if category == "Excellent":
        suggestions.append("🌟 Help your peers - teaching reinforces your own learning")
        suggestions.append("Challenge yourself with advanced topics and projects")
    elif category == "Good":
        suggestions.append("Set specific goals to reach the 'Excellent' category")
        suggestions.append("Participate in group study sessions")
    elif category == "Average":
        suggestions.append("Break down your study sessions into focused 25-minute intervals")
        suggestions.append("Use active recall and spaced repetition techniques")
    else:
        suggestions.append("Don't be discouraged - consistent effort will show results")
        suggestions.append("Start with small, achievable daily goals")
    
    return suggestions[:6]  # Return top 6 suggestions

def analyze_performance(subject_marks, attendance, study_hours, backlogs):
    """
    Complete performance analysis
    
    Returns:
        dict: analysis results with score, category, explanation, and suggestions
    """
    score = calculate_performance_score(subject_marks, attendance, study_hours, backlogs)
    category = categorize_performance(score)
    explanation = generate_explanation(score, category, subject_marks, attendance, study_hours, backlogs)
    suggestions = generate_suggestions(score, category, subject_marks, attendance, study_hours, backlogs)
    
    return {
        'score': score,
        'category': category,
        'explanation': explanation,
        'suggestions': suggestions
    }
