import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import re

class RewardFunction:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('punkt')
            nltk.download('vader_lexicon')
        
        self.sia = SentimentIntensityAnalyzer()
        
        # Politeness markers
        self.politeness_markers = {
            'please', 'thank', 'thanks', 'appreciate', 'grateful',
            'kind', 'regards', 'sincerely', 'best', 'warmly'
        }
        
        # Helpfulness indicators
        self.helpfulness_markers = {
            'help', 'assist', 'support', 'provide', 'suggest',
            'recommend', 'advise', 'guide', 'explain', 'clarify'
        }

    def calculate_politeness_score(self, text):
        """Calculate politeness score based on markers and sentiment."""
        text = text.lower()
        words = word_tokenize(text)
        
        # Count politeness markers
        politeness_count = sum(1 for word in words if any(marker in word for marker in self.politeness_markers))
        
        # Get sentiment scores
        sentiment_scores = self.sia.polarity_scores(text)
        
        # Combine markers and positive sentiment
        politeness_score = (0.7 * (politeness_count / max(len(words), 1))) + \
                          (0.3 * (sentiment_scores['pos'] - sentiment_scores['neg']))
        
        return min(max(politeness_score, 0), 1)  # Normalize to [0, 1]

    def calculate_helpfulness_score(self, text):
        """Calculate helpfulness score based on various factors."""
        text = text.lower()
        words = word_tokenize(text)
        
        # Count helpfulness markers
        helpfulness_count = sum(1 for word in words if any(marker in word for marker in self.helpfulness_markers))
        
        # Check for concrete information (numbers, specifics)
        has_numbers = bool(re.search(r'\d+', text))
        has_urls = bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
        
        # Calculate response length score (prefer medium-length responses)
        length_score = min(len(words) / 100, 1.0)
        
        # Combine factors
        helpfulness_score = (0.4 * (helpfulness_count / max(len(words), 1))) + \
                           (0.3 * length_score) + \
                           (0.15 * has_numbers) + \
                           (0.15 * has_urls)
        
        return min(max(helpfulness_score, 0), 1)  # Normalize to [0, 1]

    def calculate_total_score(self, text):
        """Calculate overall score combining politeness and helpfulness."""
        politeness = self.calculate_politeness_score(text)
        helpfulness = self.calculate_helpfulness_score(text)
        
        # Weight politeness and helpfulness equally
        total_score = 0.5 * politeness + 0.5 * helpfulness
        
        return {
            'total_score': total_score,
            'politeness_score': politeness,
            'helpfulness_score': helpfulness
        } 