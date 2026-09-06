from fastapi import FastAPI
from screener import run_screen

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Advanced Screener Running"}

@app.get("/screen")
def screen():
    results = run_screen()
    return {"count": len(results), "stocks": results}
