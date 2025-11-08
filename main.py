from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/search")
def search():
    return {"results": []}
