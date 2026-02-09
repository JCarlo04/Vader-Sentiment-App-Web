from flask import Flask, render_template, request, redirect, url_for, jsonify
from sentiment import SentimentAnalyzer
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
analyzer = SentimentAnalyzer()

# in-memory store of categorized texts
store = {"positive": [], "neutral": [], "negative": []}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", store=store)

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text", "").strip()
    if not text:
        return redirect(url_for("index"))

    # get both our adjusted compound and raw pos/neu/neg from vader
    result = analyzer.analyze_sentiment(text)  # returns {'score', 'classification'}
    vader_scores = analyzer.analyzer.polarity_scores(text)  # raw pos/neu/neg

    entry = {
        "text": text,
        "score": result["score"],
        "classification": result["classification"],
        "pos": float(vader_scores.get("pos", 0.0)),
        "neu": float(vader_scores.get("neu", 0.0)),
        "neg": float(vader_scores.get("neg", 0.0))
    }

    store[result["classification"]].insert(0, entry)  # newest first
    return redirect(url_for("index"))

@app.route("/data", methods=["GET"])
def data():
    # aggregate raw sums (kept for optional diagnostics)
    pos_sum = sum(e["pos"] for cat in store.values() for e in cat)
    neu_sum = sum(e["neu"] for cat in store.values() for e in cat)
    neg_sum = sum(e["neg"] for cat in store.values() for e in cat)

    counts = {k: len(v) for k, v in store.items()}
    total_entries = sum(counts.values())

    # If no entries, return zeros so chart shows "no data"
    if total_entries == 0:
        return jsonify({
            "pos": 0.0, "neu": 0.0, "neg": 0.0,
            "counts": counts,
            "avg_pos": 0.0, "avg_neu": 0.0, "avg_neg": 0.0
        })

    # Use counts for pie distribution so slices reflect number of texts per category
    pos_pct = counts.get("positive", 0) / total_entries
    neu_pct = counts.get("neutral", 0) / total_entries
    neg_pct = counts.get("negative", 0) / total_entries

    # Also provide averaged vader proportions per-entry (optional)
    avg_pos = pos_sum / total_entries
    avg_neu = neu_sum / total_entries
    avg_neg = neg_sum / total_entries

    return jsonify({
        "pos": pos_pct, "neu": neu_pct, "neg": neg_pct,
        "counts": counts,
        "avg_pos": avg_pos, "avg_neu": avg_neu, "avg_neg": avg_neg
    })

@app.route("/clear", methods=["POST"])
def clear():
    store["positive"].clear()
    store["neutral"].clear()
    store["negative"].clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # run from project root: python -m src.web or python src\web.py (from src)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)