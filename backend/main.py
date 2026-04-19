import spacy
import re
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import threading
import os
import nest_asyncio
from fastapi.middleware.cors import CORSMiddleware

# 0. Allow FastAPI to run inside the notebook environment
nest_asyncio.apply()

# 1. Kill any ghost servers from previous runs
os.system("fuser -k 8000/tcp")

# 2. Define the expected input data format
class TextPayload(BaseModel):
    text: str

# 3. Initialize the NLP Engine
class TextErrorDetector:
    def __init__(self):
        # Ensure the model is loaded (Make sure to run !python -m spacy download en_core_web_sm first if needed)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def analyze_text(self, text):
        doc = self.nlp(text)
        errors = []

        # Rule-Based Pattern Recognition
        if re.search(r'\s{2,}', text):
            errors.append({"type": "Structural", "issue": "Multiple consecutive spaces detected."})

        repeated_words = re.findall(r'\b(\w+)\s+\1\b', text, re.IGNORECASE)
        for word in repeated_words:
            errors.append({"type": "Structural", "issue": f"Repeated word detected: '{word}'"})

        # NLP Grammar & Syntax
        for sent in doc.sents:
            clean_sentence = sent.text.strip()
            if not clean_sentence:
                continue

            if not clean_sentence[0].isupper() and clean_sentence[0].isalpha():
                errors.append({"type": "Grammatical", "issue": f"Sentence should start with a capital letter: '{clean_sentence}'"})

            has_verb = any(token.pos_ in ["VERB", "AUX"] for token in sent)
            if not has_verb and len(sent) > 3: 
                errors.append({"type": "Grammatical", "issue": f"Possible sentence fragment (missing a main verb): '{clean_sentence}'"})

        return {
            "error_count": len(errors),
            "details": errors
        }

detector = TextErrorDetector()

# 4. Create the FastAPI App
app = FastAPI(title="NLP Text Analysis API")

# Add CORS Middleware so your Web App can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_endpoint(payload: TextPayload):
    results = detector.analyze_text(payload.text)
    return results

@app.get("/")
def home():
    return {"message": "Text Analysis API is running. Send a POST request to /analyze."}

# 5. Start the Server & Localtunnel
def run_server():
    # We use 0.0.0.0 to make it accessible to the tunnel
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# Run server in a background thread so Colab stays active
threading.Thread(target=run_server, daemon=True).start()

print("🌍 Server is warming up...")
import time
time.sleep(2) # Give uvicorn a second to bind to the port

print("🔗 Opening Tunnel...")
# Generate the localtunnel link
!npx localtunnel --port 8000