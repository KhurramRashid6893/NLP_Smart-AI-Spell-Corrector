from flask import Flask, render_template, request
import re, collections, requests, fuzzy
from flask import jsonify

app = Flask(__name__)

# --- STEP 1: Load a larger English word list (technical + scientific words) ---
url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
text = requests.get(url).text.lower()
WORDS = collections.Counter(text.split())

# --- STEP 2: Probability Function ---
def P(word, N=sum(WORDS.values())):
    return WORDS[word] / N

# --- STEP 3: Edit Distance Functions ---
def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    """Words two edits away."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def known(words):
    return set(w for w in words if w in WORDS)

# --- STEP 4: Phonetic Similarity (Soundex) ---
soundex = fuzzy.Soundex(4)

def phonetic_match(word):
    """Find phonetically similar words."""
    try:
        word_code = soundex(word)
        return [w for w in WORDS if soundex(w) == word_code]
    except Exception:
        return []

# --- STEP 5: Candidate Generator ---
def candidates(word):
    """Generate possible spelling corrections for a word."""
    return (known([word]) or
            known(edits1(word)) or
            known(edits2(word)) or
            known(phonetic_match(word)) or
            [word])

# --- STEP 6: Correction Function ---
def correct(word):
    """Return the most probable correction."""
    return max(candidates(word), key=P)

# --- STEP 7: Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    corrected_text = ""
    input_text = ""
    if request.method == "POST":
        input_text = request.form["text"]
        corrected_words = []
        for w in input_text.split():
            if w.lower() in WORDS:
                corrected_words.append(w)
            else:
                corrected_words.append(correct(w.lower()))
        corrected_text = " ".join(corrected_words)
    return render_template("index.html", corrected_text=corrected_text, input_text=input_text)


@app.route("/api/correct", methods=["POST"])
def api_correct():
    data = request.get_json()
    text = data.get("text", "")
    corrected_words = []
    for w in text.split():
        corrected_words.append(correct(w.lower()) if w.lower() not in WORDS else w)
    return jsonify({"corrected_text": " ".join(corrected_words)})

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
