# ✍️ Text Analysis & Error Detection System

A full-stack NLP application that processes textual datasets to identify grammatical inconsistencies and structural errors in real-time.

## 🚀 Overview
This system combines **Pattern Recognition (Regex)** with **Deep Learning-based NLP (spaCy)** to provide a comprehensive text-checking utility. It is served via a high-performance FastAPI backend and consumed by a modern, responsive web interface.

## 🧠 Key Features
* **Structural Detection:** Identifies repeated words and multiple consecutive spaces using regex patterns.
* **Grammatical Analysis:** Uses spaCy's dependency parsing to detect sentence fragments (missing verbs) and capitalization errors.
* **FastAPI Backend:** An asynchronous API that handles text processing and returns structured JSON error reports.
* **Web Interface:** A sleek, "Grammarly-style" web dashboard built with HTML5, CSS3, and JavaScript.

## 🛠️ Technical Stack
* **NLP Engine:** Python, spaCy (`en_core_web_sm`), Regex
* **Backend:** FastAPI, Uvicorn, CORS Middleware
* **Frontend:** JavaScript (Fetch API), HTML5, CSS3
* **Deployment:** Localtunnel (for development testing)

## 🏗️ How It Works

1. The user inputs text into the Web UI.
2. The UI sends a JSON payload to the `/analyze` endpoint.
3. The backend tokenizes the text and runs it through a series of rule-based and linguistic checks.
4. A detailed error report is returned, highlighting the type of error and the specific issue found.

## 👨‍💻 Author
**Muhammad Iman Khan** *BS Computer Science | Bahria University, Lahore*
