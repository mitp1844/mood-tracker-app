import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import random
import os

# Set page config
st.set_page_config(
    page_title="Daily Mood Tracker",
    page_icon="📊",
    layout="wide"
)

# File paths for data storage
DATA_FILE = "mood_tracker_data.json"
NOTIFICATIONS_FILE = "mood_notifications.json"

def load_data():
    """Load mood entries and notification history from files"""
    entries = []
    used_notifications = {1: [], 2: [], 3: [], 4: []}
    
    # Load mood entries
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                entries = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            entries = []
    
    # Load notification history
    if os.path.exists(NOTIFICATIONS_FILE):
        try:
            with open(NOTIFICATIONS_FILE, 'r', encoding='utf-8') as f:
                used_notifications = json.load(f)
                # Ensure all mood levels exist
                for level in [1, 2, 3, 4]:
                    if str(level) not in used_notifications:
                        used_notifications[str(level)] = []
                # Convert string keys back to integers
                used_notifications = {int(k): v for k, v in used_notifications.items()}
        except (json.JSONDecodeError, FileNotFoundError):
            used_notifications = {1: [], 2: [], 3: [], 4: []}
    
    return entries, used_notifications

def save_data(entries, used_notifications):
    """Save mood entries and notification history to files"""
    try:
        # Save mood entries
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False, default=str)
        
        # Save notification history (convert int keys to strings for JSON)
        notifications_to_save = {str(k): v for k, v in used_notifications.items()}
        with open(NOTIFICATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(notifications_to_save, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# Initialize session state with persistent data
if 'entries' not in st.session_state:
    entries, used_notifications = load_data()
    st.session_state.entries = entries
    st.session_state.used_notifications = used_notifications

if 'show_notification' not in st.session_state:
    st.session_state.show_notification = False
if 'notification_message' not in st.session_state:
    st.session_state.notification_message = ""

# Mood options
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

def get_positive_notification(average_mood, stress_level):
    """Generate unique positive notifications"""
    mood_value = MOOD_OPTIONS[average_mood]["value"]
    
    all_notifications = {
        4: [  # Great mood - 15 unique messages
            "🌟 Amazing! You're having a fantastic day! Keep up that positive energy!",
            "✨ You're absolutely glowing today! Your great mood is inspiring!",
            "🎉 What a wonderful day you're having! You're crushing it!",
            "🌈 Your positivity is off the charts! You're a mood champion!",
            "🚀 You're soaring high today! Your energy is contagious!",
            "💫 Absolutely brilliant mood today! You're radiating happiness!",
            "🌺 Your joy is beautiful to see! You're having an incredible day!",
            "⭐ Outstanding! Your positive spirit is shining so bright!",
            "🎊 Phenomenal mood today! You're living your best life!",
            "🌞 You're like sunshine today! Your happiness is infectious!",
            "🎯 Perfect mood management! You're absolutely nailing it!",
            "🏆 Champion-level positivity today! You're unstoppable!",
            "🌸 Your wonderful energy is blooming! What a magnificent day!",
            "🎨 You're painting today with the brightest colors! Spectacular!",
            "🌠 Your mood is stellar today! You're reaching for the stars!"
        ],
        3: [  # Good mood - 15 unique messages
            "😊 You're doing great today! Your positive vibes are showing!",
            "🌸 Nice work maintaining a good mood! You're handling things well!",
            "⭐ Your good energy is shining through! Keep it up!",
            "🌻 You're having a solid day! Your resilience is admirable!",
            "👍 Excellent mood balance today! You're doing wonderfully!",
            "🌿 Your positive outlook is refreshing! Great job today!",
            "💚 Loving this good energy from you! You're thriving!",
            "🌱 You're growing stronger every day! This mood shows it!",
            "☀️ Your warmth is radiating today! Beautiful positive energy!",
            "🎵 You're in harmony today! Your good mood is music to see!",
            "🌊 Riding the good vibes perfectly! You're flowing beautifully!",
            "🍀 Lucky to see you in such good spirits! Keep flourishing!",
            "🎈 Your mood is lifting everyone around you! Wonderful work!",
            "🌙 Peaceful and positive today! Your balance is inspiring!",
            "🕊️ Your calm confidence is beautiful! You're soaring today!"
        ],
        2: [  # Neutral mood - 15 unique messages
            "💪 You're staying steady today! Sometimes balance is exactly what we need!",
            "🌱 Neutral days are okay too! You're managing things just fine!",
            "🧘‍♀️ Finding your center today! Stability is a strength!",
            "⚖️ You're keeping things balanced! That takes real skill!",
            "🌿 Maintaining equilibrium today! Your steadiness is valuable!",
            "🎯 Right on target with your emotional balance! Well done!",
            "🌊 You're navigating today's waters smoothly! Great composure!",
            "🏔️ Standing strong and steady today! Your stability rocks!",
            "🌾 Growing at your own pace today! Consistency is powerful!",
            "🎨 Neutral tones can be beautiful too! You're doing just fine!",
            "🌍 Grounded and centered today! Your foundation is solid!",
            "🕯️ Calm and collected! Your inner peace is showing!",
            "🌉 Bridging emotions beautifully today! Your balance inspires!",
            "🎭 Sometimes the quiet moments are the most meaningful!",
            "🌤️ Partly cloudy can be perfect weather! You're doing great!"
        ],
        1: [  # Sad mood - 15 unique messages
            "🌅 Tomorrow is a new day! You're stronger than you know!",
            "💝 Be gentle with yourself today. You're doing the best you can!",
            "🌿 Tough days help us appreciate the good ones. You've got this!",
            "🤗 Remember: this feeling is temporary. You matter and you're valued!",
            "🌱 Even flowers need rain to grow. You're cultivating strength!",
            "💎 Pressure creates diamonds. You're becoming more resilient!",
            "🌈 After every storm comes a rainbow. Brighter days are ahead!",
            "🕊️ Your courage to feel deeply shows your beautiful heart!",
            "🌊 Waves of emotion are natural. You're riding them with grace!",
            "⭐ You're still shining, even on cloudy days! Never forget that!",
            "🌳 Deep roots grow in difficult seasons. You're getting stronger!",
            "💪 Your vulnerability today shows incredible bravery! You're amazing!",
            "🌙 Rest in knowing that dawn always comes. You're not alone!",
            "🎯 Acknowledging tough feelings is a sign of wisdom and growth!",
            "🌺 Your sensitivity is a superpower, even when it hurts!"
        ]
    }
    
    # Low stress bonus messages
    low_stress_bonus = [
        " And kudos for keeping your stress levels manageable! 🧘‍♀️",
        " Plus, you're handling stress like a pro! 💆‍♀️",
        " Your stress management skills are on point! 🎯",
        " Bonus points for staying calm under pressure! 🌊",
        " Your zen-like approach to stress is admirable! ☯️",
        " Love how you're keeping stress at bay! 🛡️",
        " Your peaceful energy shows great stress control! 🕊️",
        " Impressive stress management today! 🏆",
        " You're mastering the art of staying relaxed! 🎨",
        " Your chill vibes are absolutely perfect! ❄️"
    ]
    
    available_messages = all_notifications[mood_value]
    used_for_this_mood = st.session_state.used_notifications[mood_value]
    
    # Get unused messages
    unused_messages = [msg for msg in available_messages if msg not in used_for_this_mood]
    
    # If all messages used, reset and start over
    if not unused_messages:
        st.session_state.used_notifications[mood_value] = []
        message_to_use = random.choice(available_messages)
    else:
        message_to_use = random.choice(unused_messages)
    
    # Mark message as used
    st.session_state.used_notifications[mood_value].append(message_to_use)
    
    # Add bonus for low stress (1-2 stress level)
    if stress_level <= 2:
        message_to_use += random.choice(low_stress_bonus)
    
    return message_to_use

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
    st.title("📊 Daily Mood Tracker")
    
    # Show notification if exists
    if st.session_state.show_notification and st.session_state.notification_message:
        st.success(f"🎉 {st.session_state.notification_message}")
        if st.button("✖️ Close Notification"):
            st.session_state.show_notification = False
            st.rerun()
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        view = st.radio("Choose View:", ["📝 New Entry", "📊 Chart View", "📋 Entry History"])
    
    # New Entry View
    if view == "📝 New Entry":
        st.header("Track Your Mood")
        
        with st.form("mood_entry"):
            # Date selection
            entry_date = st.date_input("Date", value=date.today())
            
            st.subheader("Mood by Time Period")
            
            # Create columns for time slots
            cols = st.columns(3)
            mood_data = {}
            
            for i, (time_label, slot_key) in enumerate(TIME_SLOTS):
                with cols[i % 3]:
                    mood_data[slot_key] = st.selectbox(
                        time_label,
                        options=[""] + list(MOOD_OPTIONS.keys()),
                        format_func=lambda x: f"{x} {MOOD_OPTIONS[x]['label']}" if x else "Select mood",
                        key=slot_key
                    )
            
            # Additional fields
            col1, col2 = st.columns(2)
            
            with col1:
                emotions = st.text_input("Emotions Felt", placeholder="e.g., anxious, excited, calm")
                sleep_hours = st.number_input("Sleep (hours)", min_value=0.0, max_value=24.0, step=0.5, value=8.0)
            
            with col2:
                stress_level = st.selectbox("Stress Level", options=[1, 2, 3, 4, 5])
                activity = st.text_input("Activity Done", placeholder="e.g., exercise, work, socializing")
            
            notes = st.text_area("Notes / Triggers", placeholder="What affected your mood today?")
            
            submitted = st.form_submit_button("💾 Save Entry", type="primary")
            
            if submitted:
                # Calculate average mood
                entry = {
                    'date': entry_date.strftime('%Y-%m-%d'),
                    'emotions': emotions,
                    'sleep': sleep_hours,
                    'stress': stress_level,
                    'activity': activity,
                    'notes': notes
                }
                entry.update(mood_data)
                
                average_mood = calculate_average_mood(entry)
                entry['average_mood'] = average_mood
                
                # Check if entry already exists for this date
                existing_index = -1
                for i, existing_entry in enumerate(st.session_state.entries):
                    if existing_entry['date'] == entry['date']:
                        existing_index = i
                        break
                
                if existing_index >= 0:
                    st.session_state.entries[existing_index] = entry
                    # Save data to file
                    if save_data(st.session_state.entries, st.session_state.used_notifications):
                        st.success("Entry updated and saved successfully!")
                    else:
                        st.warning("Entry updated but couldn't save to file!")
                else:
                    st.session_state.entries.append(entry)
                    # Save data to file
                    if save_data(st.session_state.entries, st.session_state.used_notifications):
                        st.success("Entry saved successfully!")
                    else:
                        st.warning("Entry added but couldn't save to file!")
                
                # Show positive notification
                if average_mood:
                    notification_msg = get_positive_notification(average_mood, stress_level)
                    st.session_state.notification_message = notification_msg
                    st.session_state.show_notification = True
                    # Save updated notification history
                    save_data(st.session_state.entries, st.session_state.used_notifications)
                
                st.rerun()
    
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
                            if save_data(st.session_state.entries, st.session_state.used_notifications):
                                st.success("Entry deleted and saved!")
                            else:
                                st.warning("Entry deleted but couldn't save changes!")
                            st.rerun()
    
    # Data Management Section
    with st.sidebar:
        st.markdown("---")
        st.subheader("📁 Data Management")
        
        # Show data file status
        if os.path.exists(DATA_FILE):
            st.success("✅ Data file found")
            st.caption(f"📊 {len(st.session_state.entries)} entries saved")
        else:
            st.info("💾 No saved data yet")
        
        # Export data button
        if st.session_state.entries:
            if st.button("📤 Export Data"):
                # Create export data
                export_data = {
                    "entries": st.session_state.entries,
                    "export_date": datetime.now().isoformat(),
                    "total_entries": len(st.session_state.entries)
                }
                
                # Convert to JSON string for download
                json_str = json.dumps(export_data, indent=2, ensure_ascii=False, default=str)
                
                st.download_button(
                    label="💾 Download Backup",
                    data=json_str,
                    file_name=f"mood_tracker_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        # Clear all data button (with confirmation)
        if st.session_state.entries:
            st.markdown("---")
            if st.button("🗑️ Clear All Data", type="secondary"):
                st.warning("⚠️ This will delete all your mood entries!")
                if st.button("✅ Confirm Delete All", type="secondary"):
                    st.session_state.entries = []
                    st.session_state.used_notifications = {1: [], 2: [], 3: [], 4: []}
                    
                    # Delete data files
                    try:
                        if os.path.exists(DATA_FILE):
                            os.remove(DATA_FILE)
                        if os.path.exists(NOTIFICATIONS_FILE):
                            os.remove(NOTIFICATIONS_FILE)
                        st.success("All data cleared!")
                    except Exception as e:
                        st.error(f"Error clearing files: {e}")
                    
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tip:** Track your mood daily to identify patterns and improve your mental well-being!")

if __name__ == "__main__":
    main()