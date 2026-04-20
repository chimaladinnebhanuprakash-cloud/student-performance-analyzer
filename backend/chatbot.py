"""
AI Assistant chatbot logic for Student Performance Analyzer
Rule-based conversational AI that provides personalized guidance
"""
import random

def get_chatbot_response(message, user_profile, latest_analysis):
    """
    Generate chatbot response based on user message, profile, and performance
    
    Args:
        message: user's message
        user_profile: dict with user profile data
        latest_analysis: dict with latest performance analysis
    
    Returns:
        str: chatbot response
    """
    message_lower = message.lower()
    
    # Get user name for personalization
    user_name = user_profile.get('full_name', 'Student').split()[0] if user_profile else 'Student'
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        greetings = [
            f"Hello {user_name}! How can I help you today?",
            f"Hi {user_name}! I'm here to support your academic journey. What would you like to discuss?",
            f"Hey {user_name}! Ready to boost your performance? Ask me anything!"
        ]
        return random.choice(greetings)
    
    # Performance-related queries
    if any(word in message_lower for word in ['performance', 'score', 'how am i doing', 'progress']):
        if latest_analysis:
            category = latest_analysis.get('category', 'Unknown')
            score = latest_analysis.get('score', 0)
            
            response = f"Based on your latest analysis, {user_name}, you're performing at a '{category}' level with a score of {score}/100. "
            
            if category == "Excellent":
                response += "You're doing fantastic! Keep maintaining this excellence. 🌟"
            elif category == "Good":
                response += "You're doing well! With a bit more effort, you can reach excellence!"
            elif category == "Average":
                response += "There's definitely room for improvement. Let's work on boosting your performance!"
            else:
                response += "Don't worry, we can turn this around together! Consistency is key."
            
            return response
        else:
            return f"I don't have your performance data yet, {user_name}. Please complete a performance analysis first!"
    
    # Study tips
    if any(word in message_lower for word in ['study', 'tips', 'how to study', 'learn', 'focus']):
        tips = [
            f"Here are some effective study tips, {user_name}:\n\n1. **Pomodoro Technique**: Study for 25 minutes, then take a 5-minute break\n2. **Active Recall**: Test yourself instead of just re-reading\n3. **Spaced Repetition**: Review material at increasing intervals\n4. **Teach Others**: Explaining concepts solidifies your understanding\n5. **Eliminate Distractions**: Keep your phone away during study time",
            
            f"Great question, {user_name}! Try these proven study methods:\n\n1. **Create Mind Maps**: Visual connections help memory\n2. **Practice Problems**: Don't just read - solve!\n3. **Study Groups**: Collaborate with serious peers\n4. **Take Notes by Hand**: Writing improves retention\n5. **Get Enough Sleep**: Your brain consolidates learning during sleep",
            
            f"Let me share some study strategies, {user_name}:\n\n1. **Set Clear Goals**: Know what you want to achieve each session\n2. **Use Multiple Resources**: Books, videos, practice tests\n3. **Regular Breaks**: Don't burn out - rest is productive\n4. **Stay Organized**: Keep notes and materials well-structured\n5. **Review Regularly**: Don't wait until exams to revise"
        ]
        return random.choice(tips)
    
    # Time management
    if any(word in message_lower for word in ['time', 'manage', 'schedule', 'organize', 'plan']):
        if user_profile:
            semester = user_profile.get('semester', '')
            response = f"Time management is crucial, {user_name}! Here's a personalized schedule:\n\n"
            response += "**Daily Routine:**\n"
            response += "• Morning (6-8 AM): Review previous day's notes\n"
            response += "• Classes: Stay attentive and take notes\n"
            response += "• Afternoon (2-4 PM): Complete assignments\n"
            response += "• Evening (6-9 PM): Deep study session (3 hours)\n"
            response += "• Night (9-10 PM): Light revision or reading\n\n"
            response += "**Weekly:**\n"
            response += "• Dedicate weekends to practice problems\n"
            response += "• Review the entire week's learning on Sunday\n\n"
            response += "Remember: Consistency beats intensity!"
            return response
        else:
            return "Time management is key! Create a daily schedule, prioritize tasks, and stick to it. Would you like specific tips?"
    
    # Motivation
    if any(word in message_lower for word in ['motivate', 'motivation', 'discouraged', 'give up', 'difficult', 'hard']):
        motivational = [
            f"Listen {user_name}, every expert was once a beginner. Your struggles today are building your success tomorrow. Keep pushing! 💪",
            
            f"{user_name}, remember: 'Success is not final, failure is not fatal.' Every small step counts. You're capable of more than you think! 🌟",
            
            f"Feeling challenged is a sign you're growing, {user_name}! The difficulty you're facing now is developing your abilities. Don't give up! 🚀",
            
            f"Hey {user_name}, tough times don't last, but tough people do! Your dedication will pay off. Believe in yourself! ✨"
        ]
        return random.choice(motivational)
    
    # Exam preparation
    if any(word in message_lower for word in ['exam', 'test', 'preparation', 'prepare']):
        return f"Exam prep strategy for you, {user_name}:\n\n1. **Start Early**: Don't cram - begin 2 weeks before\n2. **Make a Checklist**: List all topics to cover\n3. **Practice Previous Papers**: Understand the pattern\n4. **Focus on Weak Areas**: Prioritize difficult topics\n5. **Take Mock Tests**: Simulate exam conditions\n6. **Stay Healthy**: Eat well, sleep 7-8 hours\n7. **Stay Positive**: Confidence matters!\n\nYou've got this! 📚"
    
    # Attendance concerns
    if any(word in message_lower for word in ['attendance', 'absent', 'bunk', 'skip']):
        if latest_analysis:
            # Check if we have attendance data from performance records
            return f"{user_name}, attendance is crucial! It directly impacts your learning and performance score. Aim for 90%+ attendance. Regular classes help you:\n• Stay updated with coursework\n• Clarify doubts immediately\n• Build rapport with teachers\n• Avoid missing important announcements\n\nMake attendance a priority!"
        else:
            return "Attendance matters! Regular attendance helps you stay on track and improves your overall performance. Aim for at least 75%, but 90%+ is ideal!"
    
    # Backlog help
    if any(word in message_lower for word in ['backlog', 'failed', 'clear', 'arrear']):
        return f"Backlogs can be cleared, {user_name}! Here's how:\n\n1. **Identify Root Cause**: Why did you struggle?\n2. **Get Help**: Consult teachers or seniors\n3. **Dedicated Time**: Allocate specific hours daily\n4. **Focus on Basics**: Build strong foundation\n5. **Practice Extensively**: Solve previous papers\n6. **Stay Determined**: You can do this!\n\nClearing backlogs will boost your confidence and performance! 💪"
    
    # Subject-specific help
    if any(word in message_lower for word in ['subject', 'math', 'science', 'physics', 'chemistry', 'programming']):
        return f"For subject-specific improvement, {user_name}:\n\n• **Identify Weak Topics**: Focus on what you struggle with\n• **Use Multiple Resources**: YouTube, textbooks, online courses\n• **Practice Daily**: Consistency is more important than intensity\n• **Join Study Groups**: Learn from peers\n• **Ask Questions**: Never hesitate to seek help\n• **Relate to Real Life**: Connect concepts to practical applications\n\nWhich subject do you need help with?"
    
    # Stress management
    if any(word in message_lower for word in ['stress', 'anxiety', 'pressure', 'overwhelmed', 'worried']):
        return f"I understand, {user_name}. Academic pressure is real. Here's how to manage:\n\n1. **Break Tasks Down**: Small steps are less overwhelming\n2. **Take Breaks**: Rest is productive, not lazy\n3. **Exercise**: Physical activity reduces stress\n4. **Talk to Someone**: Friends, family, or counselors\n5. **Practice Mindfulness**: Deep breathing helps\n6. **Maintain Perspective**: One exam doesn't define you\n\nYour mental health matters. Take care of yourself! 🌸"
    
    # Thank you
    if any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
        responses = [
            f"You're welcome, {user_name}! I'm always here to help. Keep up the great work! 😊",
            f"Happy to help, {user_name}! Remember, I'm here whenever you need guidance. Good luck! 🌟",
            f"Anytime, {user_name}! Your success is what matters. Keep pushing forward! 💪"
        ]
        return random.choice(responses)
    
    # Default response with personalized guidance
    if latest_analysis:
        category = latest_analysis.get('category', 'Unknown')
        suggestions = latest_analysis.get('suggestions', [])
        
        response = f"I'm here to help you succeed, {user_name}! "
        
        if category == "Needs Improvement":
            response += "I see you're working on improving your performance. "
        elif category == "Average":
            response += "You're doing okay, but let's aim higher! "
        elif category == "Good":
            response += "You're doing well! Let's push for excellence. "
        else:
            response += "You're excelling! Let's maintain this momentum. "
        
        if suggestions:
            response += f"\n\nHere's a key suggestion for you: {suggestions[0]}\n\n"
        
        response += "Ask me about:\n• Study tips\n• Time management\n• Exam preparation\n• Motivation\n• Specific subjects\n\nHow can I assist you today?"
        
        return response
    else:
        return f"Hello {user_name}! I'm your AI study assistant. I can help you with:\n\n• Study techniques and tips\n• Time management strategies\n• Exam preparation\n• Motivation and guidance\n• Performance improvement\n\nWhat would you like to know?"
