"""
AI Roast Generator using Groq API
Generates creative roasts with different styles and difficulty levels
"""
import os
from groq import Groq
import random
from typing import Dict, List


class RoastGenerator:
    def __init__(self, api_key: str = None):
        """
        Initialize the Roast Generator with Groq API

        Args:
            api_key: Groq API key (if None, will try to get from environment)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass it to constructor.")

        self.client = Groq(api_key=self.api_key)
        self.model = "openai/gpt-oss-120b"  # Most powerful available model (120B parameters)

        # Define roast styles
        self.styles = {
            'savage': {
                'description': 'Brutal and merciless',
                'tone': 'extremely harsh and cutting, pull no punches'
            },
            'clever': {
                'description': 'Witty and intelligent',
                'tone': 'smart and witty, using wordplay and clever observations'
            },
            'playful': {
                'description': 'Light-hearted teasing',
                'tone': 'playful and teasing, funny without being too mean'
            },
            'creative': {
                'description': 'Unexpected and original',
                'tone': 'creative and unexpected, using unique metaphors and comparisons'
            },
            'cringe': {
                'description': 'So bad it hurts',
                'tone': 'intentionally cringe-worthy and awkward, dad-joke level bad'
            }
        }

    def generate_roast(self,
                      target: str = "opponent",
                      style: str = "clever",
                      context: str = "",
                      difficulty: str = "medium") -> str:
        """
        Generate a roast using Groq API

        Args:
            target: Who/what to roast (default: "opponent")
            style: Roast style (savage/clever/playful/creative/cringe)
            context: Additional context about the target
            difficulty: AI difficulty (easy/medium/hard)

        Returns:
            Generated roast as string
        """
        # Validate style
        if style not in self.styles:
            style = "clever"

        style_info = self.styles[style]

        # Build the prompt based on difficulty
        if difficulty == "easy":
            creativity = 0.6
            instruction = "Keep it simple and straightforward."
        elif difficulty == "hard":
            creativity = 1.0
            instruction = "Be exceptionally creative and cutting-edge with your roast."
        else:  # medium
            creativity = 0.8
            instruction = "Be creative but not over the top."

        # Construct the system prompt
        system_prompt = f"""You are a master roast comedian participating in a roast battle.
Your style is {style_info['tone']}.

Rules:
- Generate ONE roast only (1-2 sentences max)
- Be {style_info['description'].lower()}
- {instruction}
- NO racism, sexism, or discriminatory content
- Focus on personality, choices, or general characteristics
- Make it funny and entertaining
- Do not use asterisks or emojis
"""

        # Construct user prompt
        user_prompt = f"Roast {target}"
        if context:
            user_prompt += f" (Context: {context})"
        user_prompt += f". Style: {style}."

        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                model=self.model,
                temperature=creativity,
                max_tokens=150,
                top_p=0.9,
            )

            roast = chat_completion.choices[0].message.content.strip()

            # Clean up the roast (remove quotes if present)
            roast = roast.strip('"').strip("'")

            return roast

        except Exception as e:
            error_msg = f"Error generating roast: {e}"
            print(error_msg)
            # Return error info with fallback
            return f"[API Error - Using Fallback] {self._get_fallback_roast(style)}"

    def _get_fallback_roast(self, style: str) -> str:
        """Fallback roasts in case API fails"""
        fallbacks = {
            'savage': [
                "You're like a participation trophy - nobody really wanted you, but here you are anyway.",
                "I'd explain how you lost this roast battle, but I don't have the crayons or the patience."
            ],
            'clever': [
                "You bring everyone so much joy - when you leave the room.",
                "You're proof that evolution can go in reverse."
            ],
            'playful': [
                "You're like a software update - nobody asked for you, but you show up anyway!",
                "I'd call you average, but that would be an insult to average people."
            ],
            'creative': [
                "You're like a cloud - when you disappear, it's a beautiful day.",
                "You have the personality of a terms and conditions agreement that nobody reads."
            ],
            'cringe': [
                "Are you a keyboard? Because you're just my type... of disappointment!",
                "If you were a vegetable, you'd be a cabbage - bland and nobody's favorite."
            ]
        }

        return random.choice(fallbacks.get(style, fallbacks['clever']))

    def generate_comeback(self, opponent_roast: str, style: str = "clever") -> str:
        """
        Generate a comeback to opponent's roast

        Args:
            opponent_roast: The roast to respond to
            style: Style of comeback

        Returns:
            Generated comeback
        """
        system_prompt = f"""You are a master roast comedian. Someone just roasted you with: "{opponent_roast}"

Generate a COMEBACK roast that:
- Turns their roast against them
- Is {self.styles[style]['tone']}
- Is 1-2 sentences max
- Is witty and funny
- Does NOT simply repeat their insult
- NO discriminatory content
"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": "Generate your comeback roast now."
                    }
                ],
                model=self.model,
                temperature=0.9,
                max_tokens=150,
            )

            comeback = chat_completion.choices[0].message.content.strip()
            comeback = comeback.strip('"').strip("'")

            return comeback

        except Exception as e:
            print(f"Error generating comeback: {e}")
            return "At least I don't need an AI to tell me I'm winning this battle."

    def get_available_styles(self) -> Dict[str, str]:
        """Return available roast styles with descriptions"""
        return {style: info['description'] for style, info in self.styles.items()}


# Test the generator
if __name__ == "__main__":
    import sys

    # Check if API key is available
    if not os.getenv("GROQ_API_KEY"):
        print("Please set GROQ_API_KEY environment variable")
        sys.exit(1)

    generator = RoastGenerator()

    print("Available styles:", generator.get_available_styles())
    print("\n" + "="*50)

    for style in ['savage', 'clever', 'playful', 'creative', 'cringe']:
        print(f"\n{style.upper()} roast:")
        roast = generator.generate_roast(
            target="my opponent",
            style=style,
            difficulty="medium"
        )
        print(f"  {roast}")
