# /// script
# dependencies = [
# "fastapi",
# "uvicorn"
# ]
# ///

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    with open("example-inner-test.py", "r") as f:
        return {"code": f.read()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
