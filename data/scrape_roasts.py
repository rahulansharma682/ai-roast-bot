"""
Roast Data Scraper
Scrapes roasts from Reddit r/RoastMe and other sources
"""
import json
import requests
from typing import List, Dict
import time

class RoastScraper:
    def __init__(self):
        self.base_url = "https://www.reddit.com/r/RoastMe"

    def scrape_reddit_roasts(self, limit: int = 100) -> List[Dict]:
        """
        Scrape roasts from Reddit r/RoastMe
        Uses Reddit's JSON API (no authentication needed for public posts)
        """
        roasts = []
        url = f"{self.base_url}/top.json?limit={limit}&t=all"

        headers = {
            'User-Agent': 'RoastBot/1.0'
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                posts = data['data']['children']

                for post in posts:
                    post_data = post['data']
                    post_id = post_data['id']

                    # Get comments for this post
                    comments_url = f"{self.base_url}/comments/{post_id}.json"
                    time.sleep(1)  # Rate limiting

                    comments_response = requests.get(comments_url, headers=headers)

                    if comments_response.status_code == 200:
                        comments_data = comments_response.json()

                        if len(comments_data) > 1:
                            comments = comments_data[1]['data']['children']

                            for comment in comments[:10]:  # Top 10 comments per post
                                if comment['kind'] == 't1':
                                    comment_body = comment['data'].get('body', '')
                                    score = comment['data'].get('score', 0)

                                    if len(comment_body) > 20 and score > 10:
                                        roasts.append({
                                            'roast': comment_body,
                                            'score': score,
                                            'source': 'reddit'
                                        })

                print(f"Scraped {len(roasts)} roasts from Reddit")

        except Exception as e:
            print(f"Error scraping Reddit: {e}")

        return roasts

    def get_sample_roasts(self) -> List[Dict]:
        """
        Returns sample roasts for immediate use
        """
        sample_roasts = [
            {"roast": "You look like you'd get winded climbing the stairs to your mom's basement.", "score": 100, "source": "sample"},
            {"roast": "Your personality is as bland as unseasoned chicken.", "score": 95, "source": "sample"},
            {"roast": "You're proof that participation trophies don't build character.", "score": 90, "source": "sample"},
            {"roast": "I'd call you a tool, but that would imply you're useful.", "score": 88, "source": "sample"},
            {"roast": "You're like a software update - nobody wants you, but you keep showing up anyway.", "score": 85, "source": "sample"},
            {"roast": "Your parents' biggest achievement is convincing you that you're special.", "score": 82, "source": "sample"},
            {"roast": "You have all the charm of a DMV waiting room.", "score": 80, "source": "sample"},
            {"roast": "If mediocrity had a face, it would be blurrier than yours.", "score": 78, "source": "sample"},
            {"roast": "You're the human equivalent of a participation award.", "score": 75, "source": "sample"},
            {"roast": "I've seen more personality in a terms and conditions agreement.", "score": 73, "source": "sample"},
            {"roast": "You're like a cloud - when you disappear, it's a beautiful day.", "score": 70, "source": "sample"},
            {"roast": "Your best feature is that you're a cautionary tale.", "score": 68, "source": "sample"},
            {"roast": "You bring everyone so much joy - when you leave the room.", "score": 65, "source": "sample"},
            {"roast": "You're the reason shampoo has instructions.", "score": 62, "source": "sample"},
            {"roast": "If you were any more plain, you'd be a white wall in an empty room.", "score": 60, "source": "sample"},
        ]
        return sample_roasts

    def save_roasts(self, roasts: List[Dict], filename: str = "roasts_dataset.json"):
        """Save roasts to JSON file"""
        filepath = f"data/{filename}"
        with open(filepath, 'w') as f:
            json.dump(roasts, f, indent=2)
        print(f"Saved {len(roasts)} roasts to {filepath}")

    def load_roasts(self, filename: str = "roasts_dataset.json") -> List[Dict]:
        """Load roasts from JSON file"""
        filepath = f"data/{filename}"
        try:
            with open(filepath, 'r') as f:
                roasts = json.load(f)
            return roasts
        except FileNotFoundError:
            print(f"File {filepath} not found. Returning sample roasts.")
            return self.get_sample_roasts()


if __name__ == "__main__":
    scraper = RoastScraper()

    # Start with sample roasts
    print("Getting sample roasts...")
    roasts = scraper.get_sample_roasts()

    # Optionally scrape from Reddit (uncomment to use)
    # print("Scraping roasts from Reddit...")
    # reddit_roasts = scraper.scrape_reddit_roasts(limit=50)
    # roasts.extend(reddit_roasts)

    scraper.save_roasts(roasts)
    print("Done!")
