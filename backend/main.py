import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 1. CORS Configuration (Crucial for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development; change to ["http://localhost:3000"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Path Resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "trainer.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 3. Models
class ValidationRequest(BaseModel):
    problem_id: int
    user_clues: List[str]

# 4. Endpoints
@app.get("/problems")
def get_all_problems():
    conn = get_db()
    try:
        rows = conn.execute("SELECT * FROM problems").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

@app.get("/problems/{p_id}")
def get_one_problem(p_id: int):
    conn = get_db()
    try:
        # Note: Changed to fetch more specific columns based on our structured scraper
        row = conn.execute("SELECT * FROM problems WHERE id = ?", (p_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Problem not found")
        return dict(row)
    finally:
        conn.close()

@app.post("/validate")
def validate_logic(req: ValidationRequest):
    conn = get_db()
    try:
        row = conn.execute("SELECT prerequisites FROM problems WHERE id = ?", (req.problem_id,)).fetchone()
        if not row:
            return {"success": False, "feedback": "Problem data missing."}
        
        truth = (row['prerequisites'] or "").lower()
        feedback = []
        
        for clue in req.user_clues:
            if clue.lower() in truth:
                feedback.append(f"✅ {clue}: Matches problem signals.")
            else:
                feedback.append(f"❌ {clue}: Not a primary signal for this problem.")
        
        return {
            "success": any(c.lower() in truth for c in req.user_clues),
            "feedback": "\n".join(feedback)
        }
    finally:
        conn.close()

@app.get("/test")
def test_db():
    try:
        # Use an absolute path to avoid "database not found" issues
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "trainer.db") 
        
        conn = sqlite3.connect(db_path)
        # Fetchone returns a tuple like (61,), so we need [0] to get the integer 61
        result = conn.execute("SELECT count(*) FROM problems").fetchone()
        conn.close()
        
        return {"count_in_db": result[0] if result else 0}
    except Exception as e:
        # This will show you the ACTUAL error in your terminal
        return {"error": str(e)}