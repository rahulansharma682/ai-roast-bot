# 🔥 AI Roast Battle Bot

An interactive AI-powered roast battle application where you compete against an AI comedian in epic roasting competitions! Built with Streamlit and powered by Groq's lightning-fast LLMs.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Groq](https://img.shields.io/badge/Groq-AI-orange.svg)

## 📸 Demo

> Add screenshots or GIF of your app here!

**Try it yourself:** Battle against an AI comedian and see who has the better burns! 🔥

## 🎯 Features

- **Multiple Roast Styles**: Choose from Savage, Clever, Playful, Creative, or Cringe
- **AI Difficulty Levels**: Battle against Easy, Medium, or Hard AI opponents
- **Real-time Scoring**: Get instant feedback on your roasts across 4 dimensions:
  - 🎨 Creativity
  - 😂 Humor
  - 💥 Impact
  - 📝 Delivery
- **Battle History**: Track your performance across multiple rounds
- **Live Statistics**: Monitor your win rate and performance
- **Beautiful UI**: Engaging Streamlit interface with custom styling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A free Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/AI-Roast-Battle-Bot.git
   cd AI-Roast-Battle-Bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Groq API key**
   - Visit [console.groq.com](https://console.groq.com)
   - Sign up for a free account
   - Generate an API key

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Start battling!**
   - Open the app in your browser (usually `http://localhost:8501`)
   - Enter your Groq API key in the sidebar
   - Type your roast and hit the Battle button!

## 📁 Project Structure

```
AI-Roast-Battle-Bot/
├── app.py                      # Main Streamlit application
├── model/
│   ├── roast_generator.py     # AI roast generation using Groq
│   └── roast_scorer.py        # Roast scoring system
├── data/
│   └── scrape_roasts.py       # Data collection utilities
├── utils/                      # Utility functions (optional)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎮 How to Play

1. **Enter API Key**: Add your Groq API key in the sidebar
2. **Choose Settings**: Select AI roast style and difficulty
3. **Write Your Roast**: Type your best roast in the text area
4. **Battle**: Click the "🔥 BATTLE! 🔥" button
5. **View Results**: See AI's roast and compare scores
6. **Keep Playing**: Try to build up your win streak!

## 💡 Tips for Great Roasts

- ✅ Use creative metaphors and comparisons
- ✅ Keep it concise (1-2 sentences)
- ✅ Employ wordplay and clever observations
- ✅ Make it funny, not just mean
- ❌ Avoid discriminatory content
- ❌ Don't just insult - be creative!

## 🔧 Advanced Usage

### Running the Roast Generator Standalone

```python
from model.roast_generator import RoastGenerator

generator = RoastGenerator(api_key="your-groq-api-key")

# Generate a roast
roast = generator.generate_roast(
    target="opponent",
    style="clever",
    difficulty="medium"
)
print(roast)
```

### Testing the Scorer

```python
from model.roast_scorer import RoastScorer

scorer = RoastScorer(api_key="your-groq-api-key")

# Score a roast
scores = scorer.score_roast("Your roast here")
print(f"Overall Score: {scores['overall']}/10")
print(f"Grade: {scores['grade']}")
```

### Collecting More Training Data

```python
from data.scrape_roasts import RoastScraper

scraper = RoastScraper()

# Get sample roasts
roasts = scraper.get_sample_roasts()

# Optionally scrape from Reddit (uncomment in the file)
# reddit_roasts = scraper.scrape_reddit_roasts(limit=50)

scraper.save_roasts(roasts)
```

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free!)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set `GROQ_API_KEY` as a secret in Streamlit Cloud settings
5. Deploy!

### Deploy to Other Platforms

- **Hugging Face Spaces**: Upload and run as a Streamlit Space
- **Render**: Deploy as a web service
- **Railway**: One-click deployment

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Llama 3.1 70B (via Groq)
- **API**: Groq API (free tier)
- **Language**: Python 3.8+

## 📊 Scoring System

Roasts are evaluated on four key dimensions:

1. **Creativity (1-10)**: Originality and unexpected elements
2. **Humor (1-10)**: How funny and entertaining it is
3. **Impact (1-10)**: How cutting and effective the roast is
4. **Delivery (1-10)**: Quality of writing and punchiness

**Overall Score** = Average of all four dimensions
**Grade** = Letter grade (S, A, B, C, D, F)

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- Add more roast styles
- Implement multiplayer mode
- Add voice synthesis for roasts
- Create a leaderboard system
- Add more sophisticated scoring algorithms
- Build a mobile app version

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is for entertainment purposes only. Roasts generated by the AI are meant to be humorous and should not be taken seriously. Please use responsibly and be respectful in real-life interactions.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for their blazing-fast LLM inference
- [Streamlit](https://streamlit.io) for the amazing web framework
- The comedy roast community for inspiration

## 📧 Contact

Questions or suggestions? Feel free to open an issue or reach out!

---

**Made with 🔥 and Python**

Happy Roasting! 🎤
