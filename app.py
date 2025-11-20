"""
AI Roast Battle Bot - Streamlit Interface
Battle against an AI in an epic roast competition!
"""
import streamlit as st
import os
from model.roast_generator import RoastGenerator
from model.roast_scorer import RoastScorer
from datetime import datetime
import random

# Page config
st.set_page_config(
    page_title="AI Roast Battle Bot",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .roast-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 18px;
        color: #ffffff;
        font-weight: 500;
        line-height: 1.6;
    }
    .user-roast {
        background: linear-gradient(135deg, #1a5490 0%, #2d6cb5 100%);
        border-left: 5px solid #4a9eff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .ai-roast {
        background: linear-gradient(135deg, #8b2525 0%, #c13636 100%);
        border-left: 5px solid #ff4a4a;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .score-card {
        padding: 15px;
        border-radius: 8px;
        background-color: #2d2d2d;
        margin: 10px 0;
    }
    .winner-banner {
        font-size: 32px;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4a4a;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'battle_history' not in st.session_state:
    st.session_state.battle_history = []
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'ai_score' not in st.session_state:
    st.session_state.ai_score = 0
if 'round_number' not in st.session_state:
    st.session_state.round_number = 0
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'scorer' not in st.session_state:
    st.session_state.scorer = None


def initialize_models(api_key: str):
    """Initialize AI models with API key"""
    try:
        st.session_state.generator = RoastGenerator(api_key=api_key)
        st.session_state.scorer = RoastScorer(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error initializing models: {e}")
        return False


def display_score_breakdown(scores: dict, label: str):
    """Display score breakdown"""
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Creativity", f"{scores['creativity']}/10")
    with col2:
        st.metric("Humor", f"{scores['humor']}/10")
    with col3:
        st.metric("Impact", f"{scores['impact']}/10")
    with col4:
        st.metric("Delivery", f"{scores['delivery']}/10")
    with col5:
        st.metric("Overall", f"{scores['overall']}/10", delta=f"Grade: {scores['grade']}")

    st.info(f"💬 Feedback: {scores['feedback']}")


def battle_round(user_roast: str, ai_style: str, difficulty: str):
    """Execute a battle round"""
    if not st.session_state.generator or not st.session_state.scorer:
        st.error("Please enter your Groq API key in the sidebar first!")
        return

    st.session_state.round_number += 1

    # Generate AI roast
    with st.spinner("🤖 AI is crafting a devastating roast..."):
        try:
            ai_roast = st.session_state.generator.generate_roast(
                target="you",
                style=ai_style,
                difficulty=difficulty
            )

            if not ai_roast or len(ai_roast.strip()) == 0:
                st.error("⚠️ AI returned an empty roast! Check your API key.")
                ai_roast = "Error: No roast generated"

        except Exception as e:
            st.error(f"❌ Error generating AI roast: {e}")
            ai_roast = f"Error: {str(e)}"

    # Display roasts
    st.markdown("---")
    st.subheader(f"⚔️ Round {st.session_state.round_number}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👤 Your Roast")
        st.markdown(f'<div class="roast-box user-roast">{user_roast}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 🤖 AI's Roast")
        st.markdown(f'<div class="roast-box ai-roast">{ai_roast}</div>', unsafe_allow_html=True)

    # Score both roasts
    with st.spinner("🎯 Judging the roasts..."):
        user_scores = st.session_state.scorer.score_roast(user_roast)
        ai_scores = st.session_state.scorer.score_roast(ai_roast)

    # Display scores
    st.markdown("---")
    st.subheader("📊 Round Scores")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👤 Your Score")
        display_score_breakdown(user_scores, "Your")

    with col2:
        st.markdown("#### 🤖 AI's Score")
        display_score_breakdown(ai_scores, "AI's")

    # Determine round winner
    if user_scores['overall'] > ai_scores['overall']:
        winner = "You"
        st.session_state.user_score += 1
        st.success("🎉 You won this round!")
    elif ai_scores['overall'] > user_scores['overall']:
        winner = "AI"
        st.session_state.ai_score += 1
        st.error("😈 AI won this round!")
    else:
        winner = "Tie"
        st.warning("🤝 It's a tie!")

    # Add to history
    st.session_state.battle_history.append({
        'round': st.session_state.round_number,
        'user_roast': user_roast,
        'ai_roast': ai_roast,
        'user_score': user_scores['overall'],
        'ai_score': ai_scores['overall'],
        'winner': winner,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # Display current standings
    st.markdown("---")
    st.subheader("🏆 Current Standings")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👤 Your Wins", st.session_state.user_score)
    with col2:
        st.metric("🤖 AI Wins", st.session_state.ai_score)
    with col3:
        st.metric("Total Rounds", st.session_state.round_number)


def main():
    # Header
    st.title("🔥 AI Roast Battle Bot 🔥")
    st.markdown("**Battle against an AI in an epic roast competition!**")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # API Key input
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Get your free API key from https://console.groq.com"
        )

        if api_key:
            if not st.session_state.generator:
                if initialize_models(api_key):
                    st.success("✅ Models initialized!")
        else:
            st.warning("Enter your Groq API key to start battling!")
            st.markdown("[Get a free Groq API key](https://console.groq.com)")

        st.markdown("---")

        # Battle settings
        st.subheader("🎮 Battle Settings")

        ai_style = st.selectbox(
            "AI Roast Style",
            options=['clever', 'savage', 'playful', 'creative', 'cringe'],
            help="Choose the AI's roasting style"
        )

        difficulty = st.selectbox(
            "AI Difficulty",
            options=['easy', 'medium', 'hard'],
            index=1,
            help="How tough should the AI be?"
        )

        st.markdown("---")

        # Stats
        st.subheader("📈 Statistics")
        st.metric("Rounds Played", st.session_state.round_number)
        st.metric("Your Wins", st.session_state.user_score)
        st.metric("AI Wins", st.session_state.ai_score)

        if st.session_state.round_number > 0:
            win_rate = (st.session_state.user_score / st.session_state.round_number) * 100
            st.metric("Your Win Rate", f"{win_rate:.1f}%")

        st.markdown("---")

        # Reset button
        if st.button("🔄 Reset Battle"):
            st.session_state.battle_history = []
            st.session_state.user_score = 0
            st.session_state.ai_score = 0
            st.session_state.round_number = 0
            st.rerun()

    # Main content
    if not api_key:
        st.info("👈 Enter your Groq API key in the sidebar to get started!")
        st.markdown("""
        ### How to Play:
        1. Get a free Groq API key from [console.groq.com](https://console.groq.com)
        2. Enter your API key in the sidebar
        3. Type your best roast in the text box
        4. Click "🔥 Battle!" to see AI's roast and get scores
        5. Try to outscore the AI!

        ### Tips for Great Roasts:
        - Be creative and use metaphors
        - Keep it punchy (1-2 sentences)
        - Use wordplay and wit
        - Make it funny, not just mean
        - Avoid being discriminatory
        """)

    else:
        # Battle interface
        st.markdown("---")

        # Use a form to handle input and clear it automatically on submit
        with st.form(key="roast_form", clear_on_submit=True):
            user_roast = st.text_area(
                "💬 Enter Your Roast:",
                placeholder="Type your most devastating roast here...",
                height=100
            )

            # Battle button (inside form)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("🔥 BATTLE! 🔥", type="primary", use_container_width=True)

            if submit_button:
                if user_roast.strip():
                    battle_round(user_roast, ai_style, difficulty)
                else:
                    st.warning("Enter a roast first!")

        # Display battle history
        if st.session_state.battle_history:
            st.markdown("---")
            st.subheader("📜 Battle History")

            for battle in reversed(st.session_state.battle_history[-5:]):  # Show last 5
                with st.expander(f"Round {battle['round']} - Winner: {battle['winner']} 🏆"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**👤 Your Roast:**")
                        st.write(battle['user_roast'])
                        st.caption(f"Score: {battle['user_score']}/10")
                    with col2:
                        st.markdown("**🤖 AI's Roast:**")
                        st.write(battle['ai_roast'])
                        st.caption(f"Score: {battle['ai_score']}/10")


if __name__ == "__main__":
    main()
