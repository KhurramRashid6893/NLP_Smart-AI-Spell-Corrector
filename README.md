# 🧠 Smart AI Spell Corrector (Flask + NLP + Norvig)

A web-based AI spell corrector built with **Flask** that uses **Norvig’s probabilistic language model**, **phonetic similarity**, and a **large English corpus** to intelligently detect and fix spelling errors — including scientific and pronunciation-based typos like:

> “photosinthesis → photosynthesis”

---

## 🚀 Features
- 🔤 **Edit Distance Correction (Multi-level)** — Suggests words based on minimal edit operations.  
- 🔊 **Phonetic Sound Matching** — Uses Soundex to detect pronunciation-based misspellings.  
- 📚 **Large English Word Corpus** — Improves accuracy through extensive vocabulary coverage.  
- 💻 **Responsive Web UI** — Built using Flask templates for smooth interaction.  

---

## 🧩 Tech Stack
**Python** • **Flask** • **NLP** • **Norvig Algorithm** • **Soundex** • **Text Processing**

---

## ⚙️ How It Works
1. **Input** a misspelled word or sentence.  
2. **Generate** candidate corrections using edit distance and phonetic similarity.  
3. **Score** candidates with a probabilistic language model.  
4. **Return** the most likely correct word(s) via the Flask web interface.

---

## 📦 Installation
```bash
git clone https://github.com/yourusername/smart-ai-spell-corrector.git
cd smart-ai-spell-corrector
pip install -r requirements.txt
python app.py
