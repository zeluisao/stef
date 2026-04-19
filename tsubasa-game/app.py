# app.py — The main game server
# Run with: python app.py
# Then open http://localhost:5000 in your browser!

from flask import Flask, render_template, request, session
from story import STORY, GUIDE_STEPS

app = Flask(__name__)
app.secret_key = "tsubasa-soccer-123"  # needed to remember the player's progress


@app.route("/")
def home():
    session.clear()
    return render_template("index.html", node=STORY["start"], node_id="start")


@app.route("/choice", methods=["POST"])
def choice():
    next_id = request.form.get("next")
    node = STORY.get(next_id)
    if node is None:
        return render_template("index.html", node=STORY["start"], node_id="start")
    return render_template("index.html", node=node, node_id=next_id)


@app.route("/guide")
def guide():
    return render_template("guide.html", steps=GUIDE_STEPS, story=STORY)


if __name__ == "__main__":
    print("⚽ Tsubasa Story Game is starting...")
    print("Open your browser at: http://localhost:5000")
    app.run(debug=True)
