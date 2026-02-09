import re

class SentimentAnalyzer:
    def __init__(self):
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def _preprocess(self, text):
        """
        Normalize elongated words and cap repeated punctuation to reduce
        over-dependence on punctuation while preserving emphasis signals.

        Returns (normalized_text, emphasis_boost)
        emphasis_boost is a small positive float reflecting extra emphasis from
        repeated letters (used to adjust the compound score).
        """
        if not text:
            return text, 0.0

        # cap repeated punctuation (limit ! and ? sequences to at most 3)
        def cap_punct(match):
            ch = match.group(0)[0]
            return ch * min(len(match.group(0)), 3)
        text = re.sub(r'([!?])\1+', cap_punct, text)

        # normalize elongated words:
        # - reduce runs of the same char longer than 2 to 2 (loooove -> loove)
        # - track repetition intensity to compute a small emphasis boost
        emphasis_boost = 0.0

        def _reduce_run(m):
            run = m.group(0)
            ch = run[0]
            run_len = len(run)
            # reduce to 2 characters
            reduced = ch * 2
            # per-run boost: small, diminishing with length (clamped)
            nonlocal emphasis_boost  # Python 3.8+; ensures modification
            boost = min(0.25, 0.05 * (run_len - 2))
            emphasis_boost += boost
            return reduced

        # iterate words and apply run reduction inside each word, but avoid changing entire numbers/tokens with punctuation
        # Use a callback so we can accumulate boost values.
        # Apply reduction for runs of 3+ identical chars (which signal emphasis)
        # Example: "loooove" -> "loove" and adds boost
        text = re.sub(r'(.)\1{2,}', _reduce_run, text)

        # Clamp total emphasis boost to a reasonable value
        emphasis_boost = min(emphasis_boost, 0.5)

        return text, emphasis_boost

    def analyze_sentiment(self, text):
        # preprocess to normalize elongations and punctuation
        normalized_text, emphasis_boost = self._preprocess(text)

        # get scores from vader
        sentiment_score = self.analyzer.polarity_scores(normalized_text)
        compound_score = float(sentiment_score.get('compound', 0.0))

        # adjust compound by emphasis_boost while preserving sign and clamping to [-1, 1]
        if compound_score != 0.0 and emphasis_boost > 0.0:
            sign = 1.0 if compound_score > 0 else -1.0
            compound_score = compound_score + sign * emphasis_boost
            compound_score = max(-1.0, min(1.0, compound_score))

        # classification thresholds same as VADER convention
        if compound_score >= 0.05:
            sentiment = 'positive'
        elif compound_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return {
            'score': round(compound_score, 4),
            'classification': sentiment
        }