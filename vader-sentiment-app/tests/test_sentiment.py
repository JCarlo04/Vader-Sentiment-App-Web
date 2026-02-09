import unittest
from src.sentiment import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        text = "I love this product! It's amazing."
        score, classification = self.analyzer.analyze_sentiment(text)
        self.assertGreater(score, 0)
        self.assertEqual(classification, 'positive')

    def test_negative_sentiment(self):
        text = "I hate this product. It's the worst."
        score, classification = self.analyzer.analyze_sentiment(text)
        self.assertLess(score, 0)
        self.assertEqual(classification, 'negative')

    def test_neutral_sentiment(self):
        text = "This product is okay."
        score, classification = self.analyzer.analyze_sentiment(text)
        self.assertEqual(score, 0)
        self.assertEqual(classification, 'neutral')

    def test_empty_string(self):
        text = ""
        score, classification = self.analyzer.analyze_sentiment(text)
        self.assertEqual(score, 0)
        self.assertEqual(classification, 'neutral')

if __name__ == '__main__':
    unittest.main()