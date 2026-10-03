# 📚 CogniSnap — AI Study Assistant

CogniSnap is a multimodal AI-powered study companion built with Streamlit, Google's Gemini 2.0 Flash model, and Telegram integration. It helps students understand complex coursework by analyzing textbook pages, handwritten notes, and PDFs, then generating structured study explanations and instant revision digests sent directly to Telegram.

---

## ✨ Features

- **Multimodal Material Analysis:** Upload textbook images, handwritten notes, or PDF documents for instant concept breakdowns.
- **AI Tutor Explanation Engine:** Translates dense academic jargon into plain language with real-world analogies and active-recall questions.
- **Telegram Revision Digests:** Generates structured summary flashcards and sends them directly to your phone via Telegram.
- **Streamlit Chat Interface:** Clean, reactive chat UI supporting both visual and text-based interactions.

---

## 🛠️ Tech Stack

- **Framework:** [Streamlit](https://streamlit.io/)
- **AI Engine:** Google Gemini SDK (`google-genai` with `gemini-2.0-flash`)
- **Messaging:** `python-telegram-bot`
- **Image Processing:** `Pillow` (PIL)
- **Language:** Python 3.10+

---

## 🚀 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/cognisnap.git](https://github.com/YOUR_USERNAME/cognisnap.git)
cd cognisnap
