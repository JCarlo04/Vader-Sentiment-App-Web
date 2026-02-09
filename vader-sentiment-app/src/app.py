try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except Exception:
    try:
        from vaderSentiment import SentimentIntensityAnalyzer
    except Exception:
        import sys
        print("Error: could not import 'vaderSentiment'.")
        print("Python executable:", sys.executable)
        print("Ensure the package is installed in this environment:")
        print("  python -m pip install vaderSentiment")
        raise

import tkinter as tk
from tkinter import ttk, messagebox

def classify_compound(compound):
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"

def update_graph(scores):
    """
    Draw a pie chart on the canvas showing pos/neu/neg proportions.
    Uses global canvas_graph.
    """
    pos = float(scores.get("pos", 0.0))
    neu = float(scores.get("neu", 0.0))
    neg = float(scores.get("neg", 0.0))

    # normalize if sums to zero
    total = pos + neu + neg
    if total <= 0:
        pos, neu, neg = 0.0, 1.0, 0.0
        total = 1.0

    pos_pct = pos / total
    neu_pct = neu / total
    neg_pct = neg / total

    canvas_graph.delete("all")

    # canvas dimensions
    c_width = int(canvas_graph.cget("width"))
    c_height = int(canvas_graph.cget("height"))

    # pie parameters (left side)
    pie_size = min(c_height - 16, 120)  # keep pie reasonably sized
    pie_x0 = 10
    pie_y0 = 8
    pie_x1 = pie_x0 + pie_size
    pie_y1 = pie_y0 + pie_size

    # start angle at 90 degrees so "Positive" appears at top (adjust visually)
    start = 90
    # Draw arcs: Tk create_arc start=deg, extent=deg (counter-clockwise from 3 o'clock)
    # convert fractions to degrees
    pos_deg = int(round(pos_pct * 360))
    neu_deg = int(round(neu_pct * 360))
    neg_deg = 360 - (pos_deg + neu_deg)  # ensure full circle

    # colors
    pos_color = "#2ecc71"
    neu_color = "#95a5a6"
    neg_color = "#e74c3c"

    # Draw positive slice
    if pos_deg > 0:
        canvas_graph.create_arc(pie_x0, pie_y0, pie_x1, pie_y1,
                                start=start, extent=pos_deg, fill=pos_color, outline="")
    start += pos_deg
    # Draw neutral slice
    if neu_deg > 0:
        canvas_graph.create_arc(pie_x0, pie_y0, pie_x1, pie_y1,
                                start=start, extent=neu_deg, fill=neu_color, outline="")
    start += neu_deg
    # Draw negative slice
    if neg_deg > 0:
        canvas_graph.create_arc(pie_x0, pie_y0, pie_x1, pie_y1,
                                start=start, extent=neg_deg, fill=neg_color, outline="")

    # Draw center label showing classification (largest slice)
    slices = [("Positive", pos_pct, pos_color), ("Neutral", neu_pct, neu_color), ("Negative", neg_pct, neg_color)]
    largest = max(slices, key=lambda s: s[1])
    class_text = largest[0]
    canvas_graph.create_text(pie_x0 + pie_size/2, pie_y0 + pie_size/2,
                             text=f"{class_text}", fill="white", font=("Segoe UI", 9, "bold"))

    # Legend / percentages to the right
    legend_x = pie_x1 + 12
    legend_y = pie_y0 + 4
    box_size = 12
    spacing = 6
    # Positive
    canvas_graph.create_rectangle(legend_x, legend_y, legend_x + box_size, legend_y + box_size, fill=pos_color, outline="")
    canvas_graph.create_text(legend_x + box_size + spacing, legend_y + box_size/2,
                             anchor="w", text=f"Positive: {pos_pct:.0%}", font=("Segoe UI", 9))
    # Neutral
    legend_y += box_size + 6
    canvas_graph.create_rectangle(legend_x, legend_y, legend_x + box_size, legend_y + box_size, fill=neu_color, outline="")
    canvas_graph.create_text(legend_x + box_size + spacing, legend_y + box_size/2,
                             anchor="w", text=f"Neutral: {neu_pct:.0%}", font=("Segoe UI", 9))
    # Negative
    legend_y += box_size + 6
    canvas_graph.create_rectangle(legend_x, legend_y, legend_x + box_size, legend_y + box_size, fill=neg_color, outline="")
    canvas_graph.create_text(legend_x + box_size + spacing, legend_y + box_size/2,
                             anchor="w", text=f"Negative: {neg_pct:.0%}", font=("Segoe UI", 9))

def analyze_text():
    text = txt_input.get("1.0", "end").strip()
    if not text:
        messagebox.showinfo("No input", "Please enter text to analyze.")
        return

    try:
        scores = analyzer.polarity_scores(text)
    except Exception as e:
        messagebox.showerror("Analysis error", f"Error analyzing text:\n{e}")
        return

    compound = scores.get("compound", 0.0)
    classification = classify_compound(compound)

    lbl_compound_value.config(text=f"{compound:.4f}")
    lbl_pos_value.config(text=str(scores.get("pos", 0.0)))
    lbl_neu_value.config(text=str(scores.get("neu", 0.0)))
    lbl_neg_value.config(text=str(scores.get("neg", 0.0)))
    lbl_class_value.config(text=classification.capitalize())

    # update the inline graph
    update_graph(scores)

def on_enter_key(event):
    analyze_text()
    return "break"

def build_gui():
    root = tk.Tk()
    root.title("VADER Sentiment Analyzer")

    frm = ttk.Frame(root, padding=12)
    frm.grid(row=0, column=0, sticky="nsew")

    ttk.Label(frm, text="Enter text to analyze:").grid(row=0, column=0, sticky="w")
    global txt_input
    txt_input = tk.Text(frm, width=60, height=6, wrap="word")
    txt_input.grid(row=1, column=0, columnspan=3, pady=(4, 8))
    txt_input.bind("<Control-Return>", on_enter_key)

    btn_analyze = ttk.Button(frm, text="Analyze", command=analyze_text)
    btn_analyze.grid(row=2, column=0, sticky="w")

    # Results
    results_frame = ttk.LabelFrame(frm, text="Results", padding=8)
    results_frame.grid(row=3, column=0, columnspan=3, pady=(8,0), sticky="ew")

    ttk.Label(results_frame, text="Compound:").grid(row=0, column=0, sticky="w")
    global lbl_compound_value
    lbl_compound_value = ttk.Label(results_frame, text="0.0000")
    lbl_compound_value.grid(row=0, column=1, sticky="w", padx=(6,20))

    ttk.Label(results_frame, text="Positive:").grid(row=0, column=2, sticky="w")
    global lbl_pos_value
    lbl_pos_value = ttk.Label(results_frame, text="0.0")
    lbl_pos_value.grid(row=0, column=3, sticky="w", padx=(6,20))

    ttk.Label(results_frame, text="Neutral:").grid(row=1, column=0, sticky="w")
    global lbl_neu_value
    lbl_neu_value = ttk.Label(results_frame, text="0.0")
    lbl_neu_value.grid(row=1, column=1, sticky="w", padx=(6,20))

    ttk.Label(results_frame, text="Negative:").grid(row=1, column=2, sticky="w")
    global lbl_neg_value
    lbl_neg_value = ttk.Label(results_frame, text="0.0")
    lbl_neg_value.grid(row=1, column=3, sticky="w", padx=(6,20))

    ttk.Label(results_frame, text="Classification:").grid(row=2, column=0, sticky="w", pady=(6,0))
    global lbl_class_value
    lbl_class_value = ttk.Label(results_frame, text="Neutral", font=("Segoe UI", 10, "bold"))
    lbl_class_value.grid(row=2, column=1, sticky="w", padx=(6,20), pady=(6,0))

    # Inline graph canvas (shows pos/neu/neg bars)
    global canvas_graph
    canvas_graph = tk.Canvas(results_frame, width=420, height=80, highlightthickness=0)
    canvas_graph.grid(row=3, column=0, columnspan=4, pady=(8,0), sticky="w")

    # Initialize graph to neutral
    update_graph({"pos": 0.0, "neu": 1.0, "neg": 0.0})

    # Make window resize nicely
    root.columnconfigure(0, weight=1)
    frm.columnconfigure(0, weight=1)
    return root

if __name__ == "__main__":
    analyzer = SentimentIntensityAnalyzer()
    app = build_gui()
    app.mainloop()