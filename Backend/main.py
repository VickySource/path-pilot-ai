from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Backend running"}

# ---------------- UPLOAD RESUME ----------------
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "message": "Resume uploaded successfully"
    }

# ---------------- SKILL GAP ----------------
@app.get("/skill-gap/{user_id}")
def skill_gap(user_id: str):
    return {
        "skills": ["Python", "AI", "ML"],
        "scores": [80, 70, 60],
        "missing_skills": ["Docker", "Kubernetes"]
    }

# ---------------- ROADMAP ----------------
@app.get("/roadmap/{user_id}")
def roadmap(user_id: str):
    return {
        "steps": [
            "Learn Python",
            "Build ML Projects",
            "Learn LangChain",
            "Deploy AI Apps"
        ]
    }

# ---------------- CHAT ----------------
@app.post("/chat")
async def chat(data: dict):
    return {
        "reply": f"AI Response to: {data['message']}"
    }