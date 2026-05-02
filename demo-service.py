from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/slow")
def slow():
    time.sleep(1.5)  # intentional latency issue
    return {"status": "slow"}