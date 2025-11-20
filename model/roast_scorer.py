"""
Roast Scoring System
Evaluates roast quality based on multiple criteria
"""
import os
from groq import Groq
import re
from typing import Dict, Tuple


class RoastScorer:
    def __init__(self, api_key: str = None):
        """
        Initialize the Roast Scorer

        Args:
            api_key: Groq API key (if None, will try to get from environment)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.model = "openai/gpt-oss-120b"  # Most powerful available model (120B parameters)
            self.use_ai = True
        else:
            self.use_ai = False
            print("Warning: No API key provided. Using rule-based scoring only.")

    def score_roast(self, roast: str) -> Dict[str, any]:
        """
        Score a roast on multiple dimensions

        Args:
            roast: The roast text to score

        Returns:
            Dictionary with scores and feedback
        """
        if self.use_ai:
            return self._ai_score(roast)
        else:
            return self._rule_based_score(roast)

    def _ai_score(self, roast: str) -> Dict[str, any]:
        """Use AI to score the roast"""
        system_prompt = """You are an expert roast battle judge. Evaluate the given roast on these criteria:

1. CREATIVITY (1-10): How original and unexpected is it?
2. HUMOR (1-10): How funny is it?
3. IMPACT (1-10): How cutting/effective is it?
4. DELIVERY (1-10): How well-written and punchy is it?

Respond ONLY in this exact format:
CREATIVITY: [score]
HUMOR: [score]
IMPACT: [score]
DELIVERY: [score]
FEEDBACK: [one sentence of constructive feedback]

Example:
CREATIVITY: 8
HUMOR: 7
IMPACT: 9
DELIVERY: 8
FEEDBACK: Great use of metaphor, but could be more concise."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Roast to evaluate: \"{roast}\""}
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=200,
            )

            response = chat_completion.choices[0].message.content.strip()

            # Parse the response
            scores = {}
            feedback = ""

            lines = response.split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().upper()
                    value = value.strip()

                    if key in ['CREATIVITY', 'HUMOR', 'IMPACT', 'DELIVERY']:
                        try:
                            scores[key.lower()] = int(value)
                        except:
                            scores[key.lower()] = 5
                    elif key == 'FEEDBACK':
                        feedback = value

            # Calculate overall score
            if scores:
                overall = sum(scores.values()) / len(scores)
            else:
                return self._rule_based_score(roast)

            return {
                'creativity': scores.get('creativity', 5),
                'humor': scores.get('humor', 5),
                'impact': scores.get('impact', 5),
                'delivery': scores.get('delivery', 5),
                'overall': round(overall, 1),
                'feedback': feedback or "Nice roast!",
                'grade': self._get_grade(overall)
            }

        except Exception as e:
            print(f"Error in AI scoring: {e}")
            return self._rule_based_score(roast)

    def _rule_based_score(self, roast: str) -> Dict[str, any]:
        """Fallback rule-based scoring"""
        scores = {
            'creativity': 5,
            'humor': 5,
            'impact': 5,
            'delivery': 5
        }

        # Length check (sweet spot is 50-150 characters)
        length = len(roast)
        if 50 <= length <= 150:
            scores['delivery'] += 2
        elif length < 20:
            scores['delivery'] -= 2
        elif length > 200:
            scores['delivery'] -= 1

        # Check for creative comparisons
        comparison_words = ['like', 'as if', 'resembles', 'looks like', 'sounds like']
        if any(word in roast.lower() for word in comparison_words):
            scores['creativity'] += 2

        # Check for wordplay/puns
        if re.search(r'\b(\w+)\b.*\b\1\b', roast.lower()):  # Repeated words (might be wordplay)
            scores['creativity'] += 1

        # Check for strong impact words
        impact_words = ['never', 'always', 'nobody', 'everyone', 'worst', 'best', 'only']
        if any(word in roast.lower() for word in impact_words):
            scores['impact'] += 1

        # Exclamation marks (but not too many)
        exclamations = roast.count('!')
        if exclamations == 1:
            scores['humor'] += 1
        elif exclamations > 2:
            scores['humor'] -= 1

        # Question format (rhetorical questions can be funny)
        if '?' in roast:
            scores['humor'] += 1

        # Cap scores at 10
        for key in scores:
            scores[key] = min(10, max(1, scores[key]))

        overall = sum(scores.values()) / len(scores)

        return {
            'creativity': scores['creativity'],
            'humor': scores['humor'],
            'impact': scores['impact'],
            'delivery': scores['delivery'],
            'overall': round(overall, 1),
            'feedback': self._generate_feedback(scores),
            'grade': self._get_grade(overall)
        }

    def _get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 9:
            return "S"  # S-tier (legendary)
        elif score >= 8:
            return "A"
        elif score >= 7:
            return "B"
        elif score >= 6:
            return "C"
        elif score >= 5:
            return "D"
        else:
            return "F"

    def _generate_feedback(self, scores: Dict[str, int]) -> str:
        """Generate feedback based on scores"""
        lowest = min(scores, key=scores.get)
        highest = max(scores, key=scores.get)

        feedback_templates = {
            'creativity': "Try using more metaphors or unexpected comparisons!",
            'humor': "Add more wit or clever wordplay to make it funnier!",
            'impact': "Make it more cutting - go for the jugular!",
            'delivery': "Work on making it more concise and punchy!"
        }

        if scores[highest] - scores[lowest] > 2:
            return f"Strong {highest}, but {feedback_templates.get(lowest, 'keep practicing!')}"
        else:
            return "Well-balanced roast! Keep it up!"

    def compare_roasts(self, roast1: str, roast2: str) -> Tuple[Dict, Dict, str]:
        """
        Compare two roasts and determine winner

        Returns:
            Tuple of (roast1_scores, roast2_scores, winner)
        """
        scores1 = self.score_roast(roast1)
        scores2 = self.score_roast(roast2)

        if scores1['overall'] > scores2['overall']:
            winner = "Roast 1"
        elif scores2['overall'] > scores1['overall']:
            winner = "Roast 2"
        else:
            winner = "Tie"

        return scores1, scores2, winner


# Test the scorer
if __name__ == "__main__":
    scorer = RoastScorer()

    test_roasts = [
        "You're like a cloud - when you disappear, it's a beautiful day.",
        "You're stupid and ugly.",
        "Your personality is as bland as unseasoned chicken cooked by someone who thinks mayo is spicy.",
    ]

    print("Testing Roast Scorer\n" + "="*50)

    for i, roast in enumerate(test_roasts, 1):
        print(f"\nRoast {i}: \"{roast}\"")
        scores = scorer.score_roast(roast)
        print(f"Overall Score: {scores['overall']}/10 (Grade: {scores['grade']})")
        print(f"Breakdown - Creativity: {scores['creativity']}, Humor: {scores['humor']}, "
              f"Impact: {scores['impact']}, Delivery: {scores['delivery']}")
        print(f"Feedback: {scores['feedback']}")
