import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import random
import os
import hashlib
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Daily Mood Tracker",
    page_icon="📊",
    layout="wide"
)

# Create data directory
DATA_DIR = "mood_tracker_users"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def hash_username(username):
    """Create a safe filename from username"""
    return hashlib.md5(username.lower().encode()).hexdigest()

def get_user_files(username):
    """Get file paths for a specific user"""
    user_hash = hash_username(username)
    return {
        'data': os.path.join(DATA_DIR, f"{user_hash}_data.json"),
        'notifications': os.path.join(DATA_DIR, f"{user_hash}_notifications.json")
    }

def load_user_data(username):
    """Load mood entries and notification history for a specific user"""
    files = get_user_files(username)
    entries = []
    used_notifications = {1: [], 2: [], 3: [], 4: []}
    
    # Load mood entries
    if os.path.exists(files['data']):
        try:
            with open(files['data'], 'r', encoding='utf-8') as f:
                entries = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            entries = []
    
    # Load notification history
    if os.path.exists(files['notifications']):
        try:
            with open(files['notifications'], 'r', encoding='utf-8') as f:
                used_notifications = json.load(f)
                # Convert string keys back to integers
                used_notifications = {int(k): v for k, v in used_notifications.items()}
        except (json.JSONDecodeError, FileNotFoundError):
            used_notifications = {1: [], 2: [], 3: [], 4: []}
    
    return entries, used_notifications

def save_user_data(username, entries, used_notifications):
    """Save mood entries and notification history for a specific user"""
    files = get_user_files(username)
    
    try:
        # Save mood entries
        with open(files['data'], 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False, default=str)
        
        # Save notification history
        notifications_to_save = {str(k): v for k, v in used_notifications.items()}
        with open(files['notifications'], 'w', encoding='utf-8') as f:
            json.dump(notifications_to_save, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def login_page():
    """Simple login/signup page with randomized welcome experience"""
    
    # Show special welcome message on first visit with random animations
    if 'welcome_shown' not in st.session_state:
        # Random welcome animations and messages
        welcome_options = [
            {
                "animation": "balloons",
                "message": "💖 Booboo you are the best and most beautiful girl ever! 💖",
                "style": "success",
                "floating_emojis": "💖💕💝"
            },
            {
                "animation": "snow", 
                "message": "💕 Sending you flying kisses and warm hugs, Booboo! 😘😘😘 💕",
                "style": "info",
                "floating_emojis": "😘💋💕"
            },
            {
                "animation": "balloons",
                "message": "🤗 Big virtual hugs for the amazing Booboo! You light up the world! 🤗✨",
                "style": "success",
                "floating_emojis": "🤗🫂💪"
            },
            {
                "animation": "snow",
                "message": "💖 BOOBOO 💖 You're absolutely wonderful and loved beyond measure! 🌟",
                "style": "warning",
                "floating_emojis": "🌟✨⭐"
            },
            {
                "animation": "balloons", 
                "message": "😘💕 Flying kisses your way, beautiful Booboo! You're incredible! 💕😘",
                "style": "info",
                "floating_emojis": "😘💋😍"
            },
            {
                "animation": "snow",
                "message": "🌺 Booboo, you're like sunshine on a cloudy day! Sending love! 🌞💕",
                "style": "success",
                "floating_emojis": "🌞🌺🌸"
            },
            {
                "animation": "balloons",
                "message": "💝 Special delivery of hugs and kisses for Booboo! You're amazing! 💝🤗",
                "style": "warning",
                "floating_emojis": "💝🎁🎉"
            }
        ]
        
        # Pick a random welcome experience
        chosen_welcome = random.choice(welcome_options)
        
        # Add floating emoji animation CSS
        floating_emoji_css = f"""
        <style>
        .floating-emoji {{
            position: fixed;
            font-size: 2rem;
            z-index: 9999;
            pointer-events: none;
            animation: float 4s ease-in-out infinite;
        }}
        
        .emoji-1 {{ 
            top: 10%; 
            left: 10%; 
            animation-delay: 0s;
            animation: float1 6s linear infinite;
        }}
        .emoji-2 {{ 
            top: 20%; 
            left: 80%; 
            animation-delay: 1s;
            animation: float2 7s linear infinite;
        }}
        .emoji-3 {{ 
            top: 60%; 
            left: 15%; 
            animation-delay: 2s;
            animation: float3 8s linear infinite;
        }}
        .emoji-4 {{ 
            top: 40%; 
            left: 85%; 
            animation-delay: 0.5s;
            animation: float4 6.5s linear infinite;
        }}
        .emoji-5 {{ 
            top: 80%; 
            left: 50%; 
            animation-delay: 1.5s;
            animation: float5 7.5s linear infinite;
        }}
        .emoji-6 {{ 
            top: 30%; 
            left: 60%; 
            animation-delay: 2.5s;
            animation: float6 6s linear infinite;
        }}
        
        @keyframes float1 {{
            0% {{ transform: translateY(100vh) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(-100vh) rotate(360deg); opacity: 0; }}
        }}
        
        @keyframes float2 {{
            0% {{ transform: translateX(100vw) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateX(-100vw) rotate(-360deg); opacity: 0; }}
        }}
        
        @keyframes float3 {{
            0% {{ transform: translateY(100vh) translateX(-50px) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(-100vh) translateX(50px) rotate(360deg); opacity: 0; }}
        }}
        
        @keyframes float4 {{
            0% {{ transform: translateY(-100vh) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(-360deg); opacity: 0; }}
        }}
        
        @keyframes float5 {{
            0% {{ transform: translateX(-100vw) scale(0.5) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            50% {{ transform: translateX(0vw) scale(1.2) rotate(180deg); }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateX(100vw) scale(0.5) rotate(360deg); opacity: 0; }}
        }}
        
        @keyframes float6 {{
            0% {{ transform: translate(0, 100vh) rotate(0deg) scale(0.8); opacity: 0; }}
            10% {{ opacity: 1; }}
            25% {{ transform: translate(-100px, 50vh) rotate(90deg) scale(1.1); }}
            50% {{ transform: translate(100px, 0vh) rotate(180deg) scale(1.3); }}
            75% {{ transform: translate(-50px, -50vh) rotate(270deg) scale(1.1); }}
            90% {{ opacity: 1; }}
            100% {{ transform: translate(0, -100vh) rotate(360deg) scale(0.8); opacity: 0; }}
        }}
        
        .pulse {{
            animation: pulse 1.5s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}
        </style>
        """
        
        # Get emojis for this welcome
        emojis = list(chosen_welcome["floating_emojis"])
        
        # Create floating emoji HTML
        floating_emoji_html = floating_emoji_css + """
        <div class="floating-emoji emoji-1">""" + emojis[0] + """</div>
        <div class="floating-emoji emoji-2">""" + emojis[1] + """</div>
        <div class="floating-emoji emoji-3">""" + emojis[2] + """</div>
        <div class="floating-emoji emoji-4">""" + emojis[0] + """</div>
        <div class="floating-emoji emoji-5">""" + emojis[1] + """</div>
        <div class="floating-emoji emoji-6">""" + emojis[2] + """</div>
        """
        
        # Display floating emojis
        st.markdown(floating_emoji_html, unsafe_allow_html=True)
        
        # Show animation
        if chosen_welcome["animation"] == "balloons":
            st.balloons()
        else:  # snow
            st.snow()
        
        # Show message with chosen style
        if chosen_welcome["style"] == "success":
            st.success(chosen_welcome["message"])
        elif chosen_welcome["style"] == "info":
            st.info(chosen_welcome["message"])
        elif chosen_welcome["style"] == "warning":
            st.warning(chosen_welcome["message"])
        
        # Additional visual elements with pulse animation
        st.markdown("""
        <div style="text-align: center; font-size: 2em; margin: 20px 0;" class="pulse">
            💕 🌟 💖 ✨ 🤗 😘 💝 🌺 💕
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.welcome_shown = True
    
    st.title("🧠 Welcome to Mood Tracker")
    st.markdown("### Track your daily mood and mental wellness")
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 New User"])
    
    with tab1:
        st.subheader("Enter your username")
        username = st.text_input("Username", key="login_username").strip()
        
        if st.button("🚀 Start Tracking", type="primary"):
            if username:
                if len(username) >= 3:
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Username must be at least 3 characters long")
            else:
                st.error("Please enter a username")
    
    with tab2:
        st.subheader("Create new account")
        new_username = st.text_input("Choose username", key="new_username").strip()
        
        if st.button("🎉 Create Account", type="primary"):
            if new_username:
                if len(new_username) >= 3:
                    # Check if user data already exists
                    files = get_user_files(new_username)
                    if os.path.exists(files['data']):
                        st.warning(f"User '{new_username}' already exists! Use the Login tab.")
                    else:
                        st.session_state.username = new_username
                        st.session_state.logged_in = True
                        st.success(f"Welcome {new_username}! Starting your mood tracking journey!")
                        st.rerun()
                else:
                    st.error("Username must be at least 3 characters long")
            else:
                st.error("Please choose a username")
    
    st.markdown("---")
    st.info("💡 **Tip:** Your username creates your personal mood tracking space. Choose something you'll remember!")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Show login page if not logged in
if not st.session_state.logged_in:
    login_page()
    st.stop()

# Load user data when logged in
if 'entries' not in st.session_state:
    entries, used_notifications = load_user_data(st.session_state.username)
    st.session_state.entries = entries
    st.session_state.used_notifications = used_notifications

if 'show_notification' not in st.session_state:
    st.session_state.show_notification = False
if 'notification_message' not in st.session_state:
    st.session_state.notification_message = ""

# Mood options and other constants (same as before)
MOOD_OPTIONS = {
    "😞": {"label": "Sad", "value": 1},
    "😐": {"label": "Neutral", "value": 2},
    "🙂": {"label": "Good", "value": 3},
    "😄": {"label": "Great", "value": 4}
}

TIME_SLOTS = [
    ("6am-9am", "mood_6_9"),
    ("9am-12pm", "mood_9_12"),
    ("12pm-3pm", "mood_12_3"),
    ("3pm-6pm", "mood_3_6"),
    ("6pm-9pm", "mood_6_9pm"),
    ("9pm-12am", "mood_9_12am")
]

def calculate_average_mood(entry):
    """Calculate average mood from time slot entries"""
    mood_values = []
    for _, slot_key in TIME_SLOTS:
        if slot_key in entry and entry[slot_key]:
            mood_values.append(MOOD_OPTIONS[entry[slot_key]]["value"])
    
    if not mood_values:
        return None
    
    avg_value = sum(mood_values) / len(mood_values)
    
    if avg_value <= 1.5:
        return "😞"
    elif avg_value <= 2.5:
        return "😐"
    elif avg_value <= 3.5:
        return "🙂"
    else:
        return "😄"

def analyze_mood_patterns(entries, current_entry):
    """Analyze user's mood patterns to provide contextual insights"""
    if len(entries) < 2:
        return {}
    
    # Sort entries by date
    sorted_entries = sorted(entries, key=lambda x: x['date'])
    recent_entries = sorted_entries[-7:]  # Last 7 days
    
    analysis = {
        'streak_info': {},
        'trend_info': {},
        'improvement_areas': [],
        'strengths': [],
        'comparison': {}
    }
    
    # Calculate streaks
    current_mood_value = MOOD_OPTIONS.get(current_entry.get('average_mood'), {}).get('value', 0)
    good_mood_streak = 0
    total_entries = len(recent_entries)
    
    for entry in reversed(recent_entries):
        mood_val = MOOD_OPTIONS.get(entry.get('average_mood'), {}).get('value', 0)
        if mood_val >= 3:  # Good or Great
            good_mood_streak += 1
        else:
            break
    
    analysis['streak_info'] = {
        'good_mood_streak': good_mood_streak,
        'total_recent_entries': total_entries
    }
    
    # Analyze trends
    if len(recent_entries) >= 3:
        recent_moods = [MOOD_OPTIONS.get(e.get('average_mood'), {}).get('value', 0) for e in recent_entries[-3:]]
        recent_stress = [e.get('stress', 3) for e in recent_entries[-3:]]
        
        mood_trend = 'improving' if recent_moods[-1] > recent_moods[0] else 'declining' if recent_moods[-1] < recent_moods[0] else 'stable'
        stress_trend = 'increasing' if recent_stress[-1] > recent_stress[0] else 'decreasing' if recent_stress[-1] < recent_stress[0] else 'stable'
        
        analysis['trend_info'] = {
            'mood_trend': mood_trend,
            'stress_trend': stress_trend,
            'avg_recent_mood': sum(recent_moods) / len(recent_moods),
            'avg_recent_stress': sum(recent_stress) / len(recent_stress)
        }
    
    # Find patterns and strengths
    sleep_data = [e.get('sleep', 0) for e in recent_entries if e.get('sleep')]
    if sleep_data:
        avg_sleep = sum(sleep_data) / len(sleep_data)
        if avg_sleep >= 7.5:
            analysis['strengths'].append('good_sleep')
        elif avg_sleep < 6:
            analysis['improvement_areas'].append('sleep')
    
    # Stress management
    stress_data = [e.get('stress', 3) for e in recent_entries]
    if stress_data:
        avg_stress = sum(stress_data) / len(stress_data)
        if avg_stress <= 2:
            analysis['strengths'].append('stress_management')
        elif avg_stress >= 4:
            analysis['improvement_areas'].append('stress')
    
    # Activity consistency
    activities = [e.get('activity', '') for e in recent_entries if e.get('activity')]
    if len(activities) >= 5:
        analysis['strengths'].append('activity_tracking')
    
    # Compare to last week
    if len(sorted_entries) >= 14:
        last_week = sorted_entries[-14:-7]
        this_week = sorted_entries[-7:]
        
        last_week_avg = sum(MOOD_OPTIONS.get(e.get('average_mood'), {}).get('value', 0) for e in last_week) / len(last_week)
        this_week_avg = sum(MOOD_OPTIONS.get(e.get('average_mood'), {}).get('value', 0) for e in this_week) / len(this_week)
        
        analysis['comparison'] = {
            'last_week_avg': last_week_avg,
            'this_week_avg': this_week_avg,
            'improvement': this_week_avg > last_week_avg
        }
    
    return analysis

def get_contextual_notification(average_mood, stress_level, current_entry, all_entries):
    """Generate genuine, contextual notifications based on real-time analysis"""
    mood_value = MOOD_OPTIONS[average_mood]["value"]
    analysis = analyze_mood_patterns(all_entries, current_entry)
    
    # Get current date and time context
    current_date = datetime.now()
    day_of_week = current_date.strftime("%A")
    is_weekend = day_of_week in ['Saturday', 'Sunday']
    is_monday = day_of_week == 'Monday'
    
    # Build personalized message components
    message_parts = []
    
    # Main mood acknowledgment
    if mood_value == 4:  # Great
        if analysis.get('streak_info', {}).get('good_mood_streak', 0) >= 3:
            message_parts.append(f"🌟 That's {analysis['streak_info']['good_mood_streak']} days of great vibes in a row! You're on fire!")
        else:
            message_parts.append("🌟 What an amazing day! Your positive energy is radiating!")
    
    elif mood_value == 3:  # Good
        if analysis.get('trend_info', {}).get('mood_trend') == 'improving':
            message_parts.append("🌸 I love seeing your mood trending upward! You're building momentum!")
        else:
            message_parts.append("🌸 Solid good mood today! You're handling life with grace!")
    
    elif mood_value == 2:  # Neutral
        if analysis.get('streak_info', {}).get('good_mood_streak', 0) > 0:
            message_parts.append("💪 Taking a breather after some good days is totally normal. You're staying balanced!")
        else:
            message_parts.append("💪 Neutral can be exactly what you need right now. You're finding your center!")
    
    else:  # Sad
        if analysis.get('trend_info', {}).get('mood_trend') == 'improving':
            message_parts.append("🌅 I know today was tough, but I can see you're working through it. That takes real strength!")
        else:
            message_parts.append("🌅 Tough days are part of the journey. You're being brave by acknowledging how you feel!")
    
    # Add pattern-based insights
    if analysis.get('strengths'):
        if 'good_sleep' in analysis['strengths']:
            message_parts.append("Your consistent good sleep is really paying off! 😴")
        if 'stress_management' in analysis['strengths'] and stress_level <= 2:
            message_parts.append("Your stress management skills are genuinely impressive! 🧘‍♀️")
        if 'activity_tracking' in analysis['strengths']:
            message_parts.append("I admire how consistently you're staying active! 🏃‍♀️")
    
    # Add contextual encouragement based on trends
    trend_info = analysis.get('trend_info', {})
    if trend_info.get('mood_trend') == 'improving':
        message_parts.append("The upward trend in your mood this week is real progress! 📈")
    elif trend_info.get('stress_trend') == 'decreasing':
        message_parts.append("You're actually managing to reduce your stress levels - that's no small feat! 📉")
    
    # Add comparison insights
    comparison = analysis.get('comparison', {})
    if comparison.get('improvement'):
        improvement = comparison['this_week_avg'] - comparison['last_week_avg']
        message_parts.append(f"You're averaging {improvement:.1f} points higher this week than last - genuine progress! 📊")
    
    # Add day-specific context
    current_hour = datetime.now().hour
    if 22 <= current_hour or current_hour < 6:  # Night time (10 PM - 6 AM)
        if mood_value >= 3:
            message_parts.append("Even at this late hour, your positive energy shines! 🌙")
        elif mood_value == 2:
            message_parts.append("Late night reflection time - sometimes neutral is perfect for winding down! 🌛")
        else:
            message_parts.append("Late nights can be tough, but you're taking care of yourself by tracking! 🌜")
    elif 6 <= current_hour < 12:  # Morning
        if mood_value >= 3:
            message_parts.append("Starting the day with good energy - that's setting yourself up for success! 🌅")
        else:
            message_parts.append("Morning check-ins help set the tone for the day! 🌄")
    elif 12 <= current_hour < 17:  # Afternoon
        if mood_value >= 3:
            message_parts.append("Keeping positive energy through the day - fantastic! ☀️")
        else:
            message_parts.append("Midday reflection shows great self-awareness! 🌞")
    elif 17 <= current_hour < 22:  # Evening
        if mood_value >= 3:
            message_parts.append("Ending the day on a positive note - beautiful! 🌇")
        else:
            message_parts.append("Evening reflection is such a healthy habit! 🌆")
    
    # Add sleep context if available
    sleep = current_entry.get('sleep')
    if sleep:
        if sleep >= 8 and mood_value >= 3:
            message_parts.append(f"That {sleep}-hour sleep is clearly working for you! 💤")
        elif sleep < 6 and mood_value <= 2:
            message_parts.append("Getting more sleep might help - your body and mind deserve that rest! 😴")
    
    # Add activity context
    activity = current_entry.get('activity', '').lower()
    if activity:
        if any(word in activity for word in ['exercise', 'walk', 'run', 'gym', 'sport']):
            message_parts.append("That physical activity is such a mood booster! 💪")
        elif any(word in activity for word in ['meditat', 'yoga', 'relax']):
            message_parts.append("Taking time for mindfulness - your mental health thanks you! 🧘‍♀️")
        elif any(word in activity for word in ['friend', 'social', 'family']):
            message_parts.append("Social connection is such powerful medicine for the soul! 👥")
    
    # Add improvement suggestions (gently)
    improvements = analysis.get('improvement_areas', [])
    if mood_value <= 2 and 'sleep' in improvements:
        message_parts.append("Consider prioritizing sleep this week - it might be the game-changer you need! 🌙")
    elif 'stress' in improvements and stress_level >= 4:
        message_parts.append("High stress is tough. Maybe try one small stress-reducing activity tomorrow? 🌿")
    
    # Combine message parts naturally
    if len(message_parts) == 1:
        final_message = message_parts[0]
    elif len(message_parts) == 2:
        final_message = f"{message_parts[0]} {message_parts[1]}"
    else:
        final_message = f"{message_parts[0]} {message_parts[1]} {message_parts[2]}"
    
    # Add encouraging close based on overall pattern
    total_entries = len(all_entries)
    if total_entries >= 7:
        final_message += f" You've been tracking for {total_entries} days - that commitment to self-awareness is genuinely admirable! 🎯"
    elif mood_value >= 3:
        final_message += " Keep nurturing that positive energy! ✨"
    else:
        final_message += " Tomorrow is a fresh start, and you've got this! 🌱"
    
    return final_message

def create_chart(df):
    """Create mood vs stress chart"""
    if df.empty:
        return None
    
    fig = go.Figure()
    
    # Add mood line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['mood_value'],
        mode='lines+markers',
        name='Average Mood',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=8),
        yaxis='y1'
    ))
    
    # Add stress line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['stress'],
        mode='lines+markers',
        name='Stress Level',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title="Mood vs Stress Trends",
        xaxis_title="Date",
        yaxis=dict(
            title="Average Mood",
            side="left",
            range=[1, 4],
            tickvals=[1, 2, 3, 4],
            ticktext=["😞", "😐", "🙂", "😄"]
        ),
        yaxis2=dict(
            title="Stress Level",
            side="right",
            overlaying="y",
            range=[1, 5]
        ),
        hovermode='x unified',
        height=400
    )
    
    return fig

# Main app
def main():
    # Header with user info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"📊 {st.session_state.username}'s Mood Tracker")
    with col2:
        if st.button("🚪 Logout"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Show notification if exists
    if st.session_state.show_notification and st.session_state.notification_message:
        st.success(f"🎉 {st.session_state.notification_message}")
        if st.button("✖️ Close Notification"):
            st.session_state.show_notification = False
            st.rerun()
    
    # Sidebar for navigation
    with st.sidebar:
        st.header(f"👋 Hello, {st.session_state.username}!")
        view = st.radio("Choose View:", ["📝 New Entry", "📊 Chart View", "📋 Entry History"])
    
    # New Entry View
    if view == "📝 New Entry":
        st.header("Track Your Mood")
        
        # Date selection (outside form for immediate response)
        entry_date = st.date_input("Date", value=date.today(), key="entry_date")
        
        # Check if entry already exists for this date
        existing_entry = None
        for entry in st.session_state.entries:
            if entry['date'] == entry_date.strftime('%Y-%m-%d'):
                existing_entry = entry
                break
        
        # Show info if entry exists
        if existing_entry:
            st.info(f"📝 Updating existing entry for {entry_date.strftime('%B %d, %Y')}")
        
        st.subheader("Mood by Time Period")
        st.caption("💡 Tip: You can fill in just one time slot and save! Come back anytime to add more.")
        
        # Create columns for time slots
        cols = st.columns(3)
        mood_data = {}
        
        for i, (time_label, slot_key) in enumerate(TIME_SLOTS):
            with cols[i % 3]:
                # Pre-fill with existing data if available
                current_value = existing_entry.get(slot_key, "") if existing_entry else ""
                
                # Use unique keys for each mood selector
                mood_data[slot_key] = st.selectbox(
                    time_label,
                    options=[""] + list(MOOD_OPTIONS.keys()),
                    format_func=lambda x: f"{x} {MOOD_OPTIONS[x]['label']}" if x else "Not filled yet",
                    key=f"{slot_key}_{entry_date}",  # Unique key per date
                    index=list([""] + list(MOOD_OPTIONS.keys())).index(current_value) if current_value in [""] + list(MOOD_OPTIONS.keys()) else 0
                )
        
        # Additional fields
        col1, col2 = st.columns(2)
        
        with col1:
            emotions = st.text_input(
                "Emotions Felt", 
                placeholder="e.g., anxious, excited, calm",
                value=existing_entry.get('emotions', '') if existing_entry else '',
                key=f"emotions_{entry_date}"
            )
            sleep_hours = st.number_input(
                "Sleep (hours)", 
                min_value=0.0, 
                max_value=24.0, 
                step=0.5, 
                value=float(existing_entry.get('sleep', 8.0)) if existing_entry and existing_entry.get('sleep') else 8.0,
                key=f"sleep_{entry_date}"
            )
        
        with col2:
            stress_level = st.selectbox(
                "Stress Level", 
                options=[1, 2, 3, 4, 5],
                index=int(existing_entry.get('stress', 1)) - 1 if existing_entry else 0,
                key=f"stress_{entry_date}"
            )
            activity = st.text_input(
                "Activity Done", 
                placeholder="e.g., exercise, work, socializing",
                value=existing_entry.get('activity', '') if existing_entry else '',
                key=f"activity_{entry_date}"
            )
        
        notes = st.text_area(
            "Notes / Triggers", 
            placeholder="What affected your mood today?",
            value=existing_entry.get('notes', '') if existing_entry else '',
            key=f"notes_{entry_date}"
        )
        
        # Save button with dynamic text (outside form)
        button_text = "💾 Update Entry" if existing_entry else "💾 Save Entry"
        
        # Initialize save status in session state if not exists
        if 'save_status' not in st.session_state:
            st.session_state.save_status = None
        
        if st.button(button_text, type="primary", key=f"save_btn_{entry_date}"):
            # Calculate average mood (only from filled slots)
            entry = {
                'date': entry_date.strftime('%Y-%m-%d'),
                'emotions': emotions,
                'sleep': sleep_hours,
                'stress': stress_level,
                'activity': activity,
                'notes': notes
            }
            entry.update(mood_data)
            
            # Calculate average mood only if at least one mood is filled
            filled_moods = [mood for mood in mood_data.values() if mood]
            if filled_moods:
                average_mood = calculate_average_mood(entry)
                entry['average_mood'] = average_mood
            else:
                entry['average_mood'] = None
            
            # Check if entry already exists for this date
            existing_index = -1
            for i, existing_entry_check in enumerate(st.session_state.entries):
                if existing_entry_check['date'] == entry['date']:
                    existing_index = i
                    break
            
            # Save the entry
            if existing_index >= 0:
                st.session_state.entries[existing_index] = entry
                save_success = save_user_data(st.session_state.username, st.session_state.entries, st.session_state.used_notifications)
                if save_success:
                    st.session_state.save_status = "✅ Entry updated and saved successfully!"
                else:
                    st.session_state.save_status = "⚠️ Entry updated but couldn't save to file!"
            else:
                st.session_state.entries.append(entry)
                save_success = save_user_data(st.session_state.username, st.session_state.entries, st.session_state.used_notifications)
                if save_success:
                    if filled_moods:
                        st.session_state.save_status = "✅ Entry saved successfully!"
                    else:
                        st.session_state.save_status = "✅ Partial entry saved! You can add mood data anytime."
                else:
                    st.session_state.save_status = "⚠️ Entry added but couldn't save to file!"
            
            # Show positive notification only if we have mood data
            if entry.get('average_mood'):
                notification_msg = get_contextual_notification(entry['average_mood'], stress_level, entry, st.session_state.entries)
                st.session_state.notification_message = notification_msg
                st.session_state.show_notification = True
                # Save updated notification history
                save_user_data(st.session_state.username, st.session_state.entries, st.session_state.used_notifications)
            elif filled_moods:
                # Show encouraging message for partial mood data without setting notification
                st.session_state.save_status += "\n🌟 Great start! Feel free to add more mood data throughout the day."
        
        # Display save status if it exists
        if st.session_state.save_status:
            if "✅" in st.session_state.save_status:
                st.success(st.session_state.save_status)
            elif "⚠️" in st.session_state.save_status:
                st.warning(st.session_state.save_status)
            else:
                st.info(st.session_state.save_status)
            
            # Clear status after showing it
            if st.button("✖️ Clear Status", key=f"clear_status_{entry_date}"):
                st.session_state.save_status = None
                st.rerun()
        
        # Add quick save info
        st.caption("✨ You can save with just partial information and update it later!")
    
    # Chart View
    elif view == "📊 Chart View":
        st.header("Mood vs Stress Trends")
        
        if not st.session_state.entries:
            st.info("No data available. Add some mood entries to see your trends!")
        else:
            # Prepare data for chart
            chart_data = []
            for entry in st.session_state.entries:
                if entry.get('average_mood'):
                    chart_data.append({
                        'date': entry['date'],
                        'mood_value': MOOD_OPTIONS[entry['average_mood']]['value'],
                        'stress': entry['stress'],
                        'average_mood': entry['average_mood']
                    })
            
            if chart_data:
                df = pd.DataFrame(chart_data)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                fig = create_chart(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                **How to read this chart:**
                - Blue line shows your average mood (😞=1, 😐=2, 🙂=3, 😄=4)
                - Red line shows your stress level (1=low, 5=high)
                - Look for patterns: Does high stress correlate with lower mood?
                """)
            else:
                st.info("No mood data available for charting. Make sure to fill in mood time slots!")
    
    # Entry History View
    elif view == "📋 Entry History":
        st.header("Mood History")
        
        if not st.session_state.entries:
            st.info("No entries yet. Click 'New Entry' to start tracking your mood!")
        else:
            # Sort entries by date (most recent first)
            sorted_entries = sorted(st.session_state.entries, key=lambda x: x['date'], reverse=True)
            
            for i, entry in enumerate(sorted_entries):
                with st.expander(f"📅 {entry['date']} - {entry.get('average_mood', '❓')} Average"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Show time slot moods
                        st.markdown("**Mood Timeline:**")
                        mood_cols = st.columns(3)
                        for j, (time_label, slot_key) in enumerate(TIME_SLOTS):
                            with mood_cols[j % 3]:
                                mood_emoji = entry.get(slot_key, '-')
                                mood_label = MOOD_OPTIONS.get(mood_emoji, {}).get('label', '')
                                st.write(f"**{time_label}:** {mood_emoji} {mood_label}")
                        
                        # Show additional info
                        st.markdown("**Details:**")
                        details_cols = st.columns(2)
                        with details_cols[0]:
                            st.write(f"**Sleep:** {entry.get('sleep', '-')} hrs")
                            st.write(f"**Emotions:** {entry.get('emotions', '-')}")
                        with details_cols[1]:
                            st.write(f"**Stress:** {entry.get('stress', '-')}/5")
                            st.write(f"**Activity:** {entry.get('activity', '-')}")
                        
                        if entry.get('notes'):
                            st.markdown(f"**Notes:** {entry['notes']}")
                    
                    with col2:
                        if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                            st.session_state.entries.remove(entry)
                            # Save data after deletion
                            if save_user_data(st.session_state.username, st.session_state.entries, st.session_state.used_notifications):
                                st.success("Entry deleted and saved!")
                            else:
                                st.warning("Entry deleted but couldn't save changes!")
                            st.rerun()
    
    # Data Management Section
    with st.sidebar:
        st.markdown("---")
        st.subheader("📁 Data Management")
        
        # Show data file status
        files = get_user_files(st.session_state.username)
        if os.path.exists(files['data']):
            st.success("✅ Data file found")
            st.caption(f"📊 {len(st.session_state.entries)} entries saved")
        else:
            st.info("💾 No saved data yet")
        
        # Export data button
        if st.session_state.entries:
            if st.button("📤 Export Data"):
                # Prepare data for Excel export
                export_data = []
                
                for entry in sorted(st.session_state.entries, key=lambda x: x['date']):
                    # Convert mood emojis to readable text
                    mood_mapping = {"😞": "Sad", "😐": "Neutral", "🙂": "Good", "😄": "Great"}
                    
                    row = {
                        'Date': entry['date'],
                        'Average Mood': mood_mapping.get(entry.get('average_mood', ''), entry.get('average_mood', '')),
                        '6am-9am': mood_mapping.get(entry.get('mood_6_9', ''), entry.get('mood_6_9', '')),
                        '9am-12pm': mood_mapping.get(entry.get('mood_9_12', ''), entry.get('mood_9_12', '')),
                        '12pm-3pm': mood_mapping.get(entry.get('mood_12_3', ''), entry.get('mood_12_3', '')),
                        '3pm-6pm': mood_mapping.get(entry.get('mood_3_6', ''), entry.get('mood_3_6', '')),
                        '6pm-9pm': mood_mapping.get(entry.get('mood_6_9pm', ''), entry.get('mood_6_9pm', '')),
                        '9pm-12am': mood_mapping.get(entry.get('mood_9_12am', ''), entry.get('mood_9_12am', '')),
                        'Sleep Hours': entry.get('sleep', ''),
                        'Stress Level': entry.get('stress', ''),
                        'Emotions': entry.get('emotions', ''),
                        'Activity': entry.get('activity', ''),
                        'Notes': entry.get('notes', '')
                    }
                    export_data.append(row)
                
                # Create DataFrame
                df = pd.DataFrame(export_data)
                
                # Create Excel file using openpyxl (simpler, no extra dependencies)
                output = BytesIO()
                
                try:
                    # Try to create Excel with basic formatting
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        # Main data sheet
                        df.to_excel(writer, sheet_name='Mood Data', index=False)
                        
                        # Summary statistics sheet
                        if len(df) > 0:
                            summary_data = {
                                'Metric': [
                                    'Total Entries',
                                    'Date Range', 
                                    'Most Common Mood',
                                    'Average Stress Level',
                                    'Average Sleep Hours',
                                    'Days Tracked',
                                    'Good/Great Days (%)',
                                    'Low Stress Days (%)'
                                ],
                                'Value': []
                            }
                            
                            # Calculate summary statistics
                            total_entries = len(df)
                            date_range = f"{df['Date'].min()} to {df['Date'].max()}"
                            
                            # Most common average mood
                            mood_counts = df['Average Mood'].value_counts()
                            most_common_mood = mood_counts.index[0] if len(mood_counts) > 0 else 'N/A'
                            
                            # Average stress (excluding empty values)
                            stress_values = [x for x in df['Stress Level'] if pd.notna(x) and x != '']
                            avg_stress = round(sum(stress_values) / len(stress_values), 1) if stress_values else 'N/A'
                            
                            # Average sleep (excluding empty values)
                            sleep_values = [float(x) for x in df['Sleep Hours'] if pd.notna(x) and x != '']
                            avg_sleep = round(sum(sleep_values) / len(sleep_values), 1) if sleep_values else 'N/A'
                            
                            # Days tracked
                            days_tracked = len(df['Date'].unique())
                            
                            # Good/Great days percentage
                            good_days = len(df[df['Average Mood'].isin(['Good', 'Great'])])
                            good_days_pct = round((good_days / total_entries) * 100, 1) if total_entries > 0 else 0
                            
                            # Low stress days percentage
                            low_stress_days = len(df[df['Stress Level'].isin([1, 2])])
                            low_stress_pct = round((low_stress_days / total_entries) * 100, 1) if total_entries > 0 else 0
                            
                            summary_data['Value'] = [
                                total_entries,
                                date_range,
                                most_common_mood,
                                avg_stress,
                                avg_sleep,
                                days_tracked,
                                f"{good_days_pct}%",
                                f"{low_stress_pct}%"
                            ]
                            
                            summary_df = pd.DataFrame(summary_data)
                            summary_df.to_excel(writer, sheet_name='Summary', index=False)
                    
                    # Get the Excel data
                    excel_data = output.getvalue()
                    
                    # Create download button
                    st.download_button(
                        label="📊 Download Excel Report",
                        data=excel_data,
                        file_name=f"mood_tracker_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                except Exception as e:
                    # Fallback to CSV if Excel fails
                    st.warning("Excel export not available, downloading as CSV instead.")
                    csv_data = df.to_csv(index=False)
                    
                    st.download_button(
                        label="📊 Download CSV Report",
                        data=csv_data,
                        file_name=f"mood_tracker_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tip:** Track your mood daily to identify patterns and improve your mental well-being!")

if __name__ == "__main__":
    main()
